# -*- encoding: utf-8 -*-
# freecell_solver v0.4.0
# Freecell Solver bindings
# Copyright © 2020, Shlomi Fish.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the author of this software nor the names of
#    contributors to this software may be used to endorse or promote
#    products derived from this software without specific prior written
#    consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Freecell Solver bindings

:Copyright: © 2020, Shlomi Fish.
:License: BSD (see /LICENSE).
"""

__title__ = 'freecell_solver'
__version__ = '0.4.0'
__author__ = 'Shlomi Fish'
__license__ = '3-clause BSD'
__docformat__ = 'restructuredtext en'

__all__ = ()

# import gettext
# G = gettext.translation('freecell_solver', '/usr/share/locale', fallback='C')
# _ = G.gettext
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under the terms of the Expat license.

import platform

from cffi import FFI


class FreecellSolver(object):
    # TEST:$num_befs_weights=5;
    NUM_BEFS_WEIGHTS = 5
    FCS_STATE_SUSPEND_PROCESS = 5

    def __init__(self, ffi=None, lib=None):
        self.user = None
        if ffi:
            self.ffi = ffi
            self.lib = lib
        else:
            self.ffi = FFI()
            self.lib = self.ffi.dlopen(
                "libfreecell-solver." + (
                    "dll" if (platform.system() == 'Windows') else "so.0"))
            if not self.lib:
                self.ffi = None
                raise ImportError("Could not find shared library")
            self.ffi.cdef('''
void * freecell_solver_user_alloc();
typedef  struct{ char s[20];}fcs_move_t;
int freecell_solver_user_get_moves_left (void * user);
int freecell_solver_user_get_next_move (void * user, fcs_move_t * move);
void freecell_solver_user_free(void * instance);
typedef char * freecell_solver_str_t;
typedef int (*freecell_solver_user_cmd_line_known_commands_callback_t)(
    void *instance, int argc, freecell_solver_str_t argv[], int arg_index,
    int *num_to_skip, int *ret, void *context);
int freecell_solver_user_cmd_line_parse_args_with_file_nesting_count(
    void *instance,
    int argc, freecell_solver_str_t argv[], int start_arg,
    freecell_solver_str_t *known_parameters,
    freecell_solver_user_cmd_line_known_commands_callback_t callback,
    void *callback_context, char **error_string,
    int *last_arg, int file_nesting_count,
    freecell_solver_str_t opened_files_dir);
int freecell_solver_user_set_flares_plan(void * instance, char * s);
long freecell_solver_user_get_num_times_long(void * user);
long freecell_solver_user_get_num_states_in_collection_long(void * user);
void freecell_solver_user_limit_iterations_long(
    void * api_instance, const long max_iters);
int freecell_solver_user_solve_board(void *api_instance,
const char *const state_as_string);
int freecell_solver_user_resume_solution(void * user);
void freecell_solver_user_recycle(void *api_instance);
''')
        self.user = self.lib.freecell_solver_user_alloc()

    def new_fcs_user_handle(self):
        return self.__class__(ffi=self.ffi, lib=self.lib)

    def ret_code_is_suspend(self, ret_code):
        """docstring for ret_code_is_suspend"""
        return ret_code == self.FCS_STATE_SUSPEND_PROCESS

    def get_next_move(self):
        move = self.ffi.new('fcs_move_t *')
        num_moves = self.lib.freecell_solver_user_get_moves_left(self.user)
        if not num_moves:
            return None
        ret = self.lib.freecell_solver_user_get_next_move(self.user, move)
        success = 0
        return (move if ret == success else None)

    def input_cmd_line(self, cmd_line_args):
        last_arg = self.ffi.new('int *')
        error_string = self.ffi.new('char * *')
        known_params = self.ffi.new('char * *')
        opened_files_dir = self.ffi.new('char [32001]')

        prefix = 'freecell_solver_user_cmd_line'
        func = 'parse_args_with_file_nesting_count'

        getattr(self.lib, prefix + '_' + func)(
            self.user,  # instance
            len(cmd_line_args),    # argc
            [self.ffi.new('char[]', bytes(s, 'UTF-8')) \
             for s in cmd_line_args],  # argv
            0,   # start_arg
            known_params,  # known_params
            self.ffi.NULL,   # callback
            self.ffi.NULL,   # callback_context
            error_string,  # error_string
            last_arg,   # last_arg
            -1,  # file_nesting_count
            opened_files_dir
        )

        return {'last_arg': last_arg[0],
                'cmd_line_args_len': len(cmd_line_args)}

    def __del__(self):
        if self.user:
            self.lib.freecell_solver_user_free(self.user)
            self.user = None

    def solve_board(self, board):
        return self.lib.freecell_solver_user_solve_board(
            self.user,
            bytes(board, 'UTF-8')
        )

    def resume_solution(self):
        return self.lib.freecell_solver_user_resume_solution(self.user)

    def limit_iterations(self, max_iters):
        self.lib.freecell_solver_user_limit_iterations_long(
            self.user,
            max_iters
        )

    def get_num_times(self):
        return self.lib.freecell_solver_user_get_num_times_long(
            self.user)

    def get_num_states_in_collection(self):
        return self.lib.freecell_solver_user_get_num_states_in_collection_long(
            self.user)

    def recycle(self):
        self.lib.freecell_solver_user_recycle(self.user)
