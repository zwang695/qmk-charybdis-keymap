/* Copyright 2026 Zachary Wang
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 */

#pragma once

#define TAPPING_TERM 250
#define QUICK_TAP_TERM 150
#define FLOW_TAP_TERM 100
#define FLOW_TAP_TERM_INDEX_SHIFT 50
#define PERMISSIVE_HOLD
#define CHORDAL_HOLD
#define SPECULATIVE_HOLD
#define DUMMY_MOD_NEUTRALIZER_KEYCODE KC_F18
#define MODS_TO_NEUTRALIZE { MOD_BIT(KC_LEFT_ALT), MOD_BIT(KC_RIGHT_ALT), MOD_BIT(KC_LEFT_GUI), MOD_BIT(KC_RIGHT_GUI) }
#define CAPS_WORD_IDLE_TIMEOUT 5000
#define SELECT_WORD_OS_MAC
#define CHARYBDIS_DRAGSCROLL_REVERSE_X
#define CHARYBDIS_DRAGSCROLL_REVERSE_Y
#define RGB_MATRIX_STARTUP_SPD 60
