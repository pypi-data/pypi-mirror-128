# Copyright 2021 Yan Yan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import torch
from torch import nn
from torch.autograd import Function
from typing import Optional, TypeVar
from spconv.tools import CUDAKernelTimer
from spconv.pytorch import ops
from spconv.pytorch.constants import PYTORCH_VERSION

from torch.autograd.function import once_differentiable
import numpy as np

from typing import List

_T = TypeVar("_T")

def identity_decorator(func: _T) -> _T:
    return func

if PYTORCH_VERSION >= [1, 6, 0]:
    import torch.cuda.amp as amp
    _TORCH_CUSTOM_FWD = amp.custom_fwd(cast_inputs=torch.float16)
    _TORCH_CUSTOM_BWD = amp.custom_bwd

else:
    _TORCH_CUSTOM_FWD = identity_decorator
    _TORCH_CUSTOM_BWD = identity_decorator

class SparseConvFunction(Function):
    @staticmethod
    @_TORCH_CUSTOM_FWD
    def forward(ctx,
                features,
                filters,
                indice_pairs,
                indice_pair_num,
                num_activate_out,
                algo,
                timer: CUDAKernelTimer = CUDAKernelTimer(False)):
        ctx.save_for_backward(indice_pairs, indice_pair_num, features, filters)
        ctx.algo = algo
        ctx.timer = timer
        return ops.indice_conv(features,
                               filters,
                               indice_pairs,
                               indice_pair_num,
                               num_activate_out,
                               False,
                               algo=algo,
                               timer=timer)

    @staticmethod
    @once_differentiable
    @_TORCH_CUSTOM_BWD
    def backward(ctx, grad_output):
        indice_pairs, indice_pair_num, features, filters = ctx.saved_tensors
        timer = ctx.timer

        input_bp, filters_bp = ops.indice_conv_backward(features,
                                                        filters,
                                                        grad_output,
                                                        indice_pairs,
                                                        indice_pair_num,
                                                        False,
                                                        algo=ctx.algo,
                                                        timer=timer)

        return input_bp, filters_bp, None, None, None, None, None


class SparseInverseConvFunction(Function):
    @staticmethod
    @_TORCH_CUSTOM_FWD
    def forward(ctx,
                features,
                filters,
                indice_pairs,
                indice_pair_num,
                num_activate_out,
                algo,
                timer: CUDAKernelTimer = CUDAKernelTimer(False)):
        ctx.save_for_backward(indice_pairs, indice_pair_num, features, filters)
        ctx.algo = algo
        ctx.timer = timer

        return ops.indice_conv(features,
                               filters,
                               indice_pairs,
                               indice_pair_num,
                               num_activate_out,
                               True,
                               False,
                               algo=algo,
                               timer=timer)

    @staticmethod
    @once_differentiable
    @_TORCH_CUSTOM_BWD
    def backward(ctx, grad_output):
        indice_pairs, indice_pair_num, features, filters = ctx.saved_tensors
        timer = ctx.timer

        input_bp, filters_bp = ops.indice_conv_backward(features,
                                                        filters,
                                                        grad_output,
                                                        indice_pairs,
                                                        indice_pair_num,
                                                        True,
                                                        False,
                                                        algo=ctx.algo,
                                                        timer=timer)

        return input_bp, filters_bp, None, None, None, None, None


class SparseImplicitGemmFunction(Function):
    @staticmethod
    @_TORCH_CUSTOM_FWD
    def forward(ctx,
                features: torch.Tensor,
                filters: torch.Tensor,
                pair_fwd: torch.Tensor,
                pair_bwd: torch.Tensor,
                pair_mask_fwd_splits: List[torch.Tensor],
                pair_mask_bwd_splits: List[torch.Tensor],
                mask_argsort_fwd_splits: List[torch.Tensor],
                mask_argsort_bwd_splits: List[torch.Tensor],
                num_activate_out: int,
                masks: List[np.ndarray],
                is_train: bool,
                is_subm: bool,
                timer: CUDAKernelTimer = CUDAKernelTimer(False)):

        out, mask_out, mask_width = ops.implicit_gemm(features, filters,
                                                      pair_fwd,
                                                      pair_mask_fwd_splits,
                                                      mask_argsort_fwd_splits,
                                                      num_activate_out, masks,
                                                      is_train, is_subm, timer)
        ctx.save_for_backward(features, filters, pair_fwd, pair_bwd)
        ctx.mask_width = mask_width
        ctx.mask_out = mask_out
        ctx.timer = timer
        ctx.pair_mask_fwd_splits = pair_mask_fwd_splits
        ctx.mask_argsort_fwd_splits = mask_argsort_fwd_splits
        ctx.pair_mask_bwd_splits = pair_mask_bwd_splits
        ctx.mask_argsort_bwd_splits = mask_argsort_bwd_splits
        # ctx.num_activate_out = num_activate_out
        ctx.masks = masks
        ctx.is_subm = is_subm
        return out

    @staticmethod
    @once_differentiable
    @_TORCH_CUSTOM_BWD
    def backward(ctx, grad_output):
        features, filters, pair_fwd, pair_bwd = ctx.saved_tensors
        mask_width = ctx.mask_width
        mask_out = ctx.mask_out
        pair_mask_fwd_splits = ctx.pair_mask_fwd_splits
        mask_argsort_fwd_splits = ctx.mask_argsort_fwd_splits
        pair_mask_bwd_splits = ctx.pair_mask_bwd_splits
        mask_argsort_bwd_splits = ctx.mask_argsort_bwd_splits
        # num_activate_out = ctx.num_activate_out
        masks = ctx.masks
        is_subm = ctx.is_subm
        timer = ctx.timer
        input_bp, filters_bp = ops.implicit_gemm_backward(
            features,
            filters,
            grad_output,
            pair_fwd,
            pair_bwd,
            pair_mask_fwd_splits,
            pair_mask_bwd_splits,
            mask_argsort_fwd_splits,
            mask_argsort_bwd_splits,
            mask_output_fwd=mask_out,
            masks=masks,
            mask_width=mask_width,
            is_subm=is_subm,
            timer=timer)
        None_9 = [None] * 11
        return (input_bp, filters_bp, *None_9)


class SubMConvFunction(Function):
    @staticmethod
    @_TORCH_CUSTOM_FWD
    def forward(ctx,
                features,
                filters,
                indice_pairs,
                indice_pair_num,
                num_activate_out,
                algo,
                timer: CUDAKernelTimer = CUDAKernelTimer(False)):
        ctx.save_for_backward(indice_pairs, indice_pair_num, features, filters)
        ctx.algo = algo
        ctx.timer = timer
        return ops.indice_conv(features,
                               filters,
                               indice_pairs,
                               indice_pair_num,
                               num_activate_out,
                               False,
                               True,
                               algo=algo,
                               timer=timer)

    @staticmethod
    @once_differentiable
    @_TORCH_CUSTOM_BWD
    def backward(ctx, grad_output):
        indice_pairs, indice_pair_num, features, filters = ctx.saved_tensors
        timer = ctx.timer

        input_bp, filters_bp = ops.indice_conv_backward(features,
                                                        filters,
                                                        grad_output,
                                                        indice_pairs,
                                                        indice_pair_num,
                                                        False,
                                                        True,
                                                        algo=ctx.algo,
                                                        timer=timer)

        return input_bp, filters_bp, None, None, None, None, None


class SparseMaxPoolFunction(Function):
    @staticmethod
    @_TORCH_CUSTOM_FWD
    def forward(ctx, features, indice_pairs, indice_pair_num,
                num_activate_out):
        out = ops.indice_maxpool(features, indice_pairs, indice_pair_num,
                                 num_activate_out)
        ctx.save_for_backward(indice_pairs, indice_pair_num, features, out)
        return out

    @staticmethod
    @once_differentiable
    @_TORCH_CUSTOM_BWD
    def backward(ctx, grad_output):
        indice_pairs, indice_pair_num, features, out = ctx.saved_tensors
        input_bp = ops.indice_maxpool_backward(features, out, grad_output,
                                               indice_pairs, indice_pair_num)
        return input_bp, None, None, None


class SparseMaxPoolImplicitGemmFunction(Function):
    @staticmethod
    @_TORCH_CUSTOM_FWD
    def forward(ctx, features: torch.Tensor, indice_pairs_fwd: torch.Tensor,
                indice_pairs_bwd: torch.Tensor, num_activate_out: int):
        out = ops.indice_maxpool_implicit_gemm(features, indice_pairs_fwd,
                                               num_activate_out)
        ctx.save_for_backward(indice_pairs_bwd, features, out)
        return out

    @staticmethod
    @once_differentiable
    @_TORCH_CUSTOM_BWD
    def backward(ctx, grad_output):
        indice_pairs_bwd, features, out = ctx.saved_tensors
        input_bp = ops.indice_maxpool_implicit_gemm_backward(
            features, out, grad_output, indice_pairs_bwd)
        return input_bp, None, None, None


indice_conv = SparseConvFunction.apply
implicit_gemm = SparseImplicitGemmFunction.apply
indice_inverse_conv = SparseInverseConvFunction.apply
indice_subm_conv = SubMConvFunction.apply
indice_maxpool = SparseMaxPoolFunction.apply
indice_maxpool_implicit_gemm = SparseMaxPoolImplicitGemmFunction.apply
