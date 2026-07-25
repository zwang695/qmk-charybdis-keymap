/* Copyright 2026 Zachary Wang
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 */

#include QMK_KEYBOARD_H

enum layers { L_BASE, L_CURSOR, L_SYM, L_NUM, L_MAGIC };
enum custom_keycodes { ARROW = SAFE_RANGE, SRCHSEL, RGB_SLD, HSV_0_0_255, HSV_0_255_255, HSV_74_255_255, HSV_169_255_255 };

#define CTL_A LCTL_T(KC_A)
#define OPT_S LALT_T(KC_S)
#define CMD_D LGUI_T(KC_D)
#define SYM_F LT(L_SYM, KC_F)
#define SYM_J LT(L_SYM, KC_J)
#define CMD_K RGUI_T(KC_K)
#define OPT_L LALT_T(KC_L)
#define CTL_SCLN RCTL_T(KC_SCLN)

const char chordal_hold_layout[MATRIX_ROWS][MATRIX_COLS] PROGMEM = LAYOUT(
    '*', 'L', 'L', 'L', 'L', 'L',       'R', 'R', 'R', 'R', 'R', '*',
    '*', 'L', 'L', 'L', 'L', 'L',       'R', 'R', 'R', 'R', 'R', '*',
    '*', 'L', 'L', 'L', 'L', 'L',       'R', 'R', 'R', 'R', 'R', '*',
    '*', 'L', 'L', 'L', 'L', 'L',       'R', 'R', 'R', 'R', 'R', '*',
                                  '*', '*', '*', '*', '*',
                                  '*', '*', '*'
);

static bool is_voyager_flow_tap_key(uint16_t keycode) {
    switch (keycode) {
        case CTL_A: case OPT_S: case CMD_D: case SYM_F:
        case SYM_J: case CMD_K: case OPT_L: case CTL_SCLN: return true;
    }
    return false;
}

bool get_speculative_hold(uint16_t keycode, keyrecord_t *record) {
    (void)record;
    return is_voyager_flow_tap_key(keycode);
}

uint16_t get_flow_tap_term(uint16_t keycode, keyrecord_t *record, uint16_t prev_keycode) {
    (void)record;
    if (!is_voyager_flow_tap_key(prev_keycode)) return 0;
    return (keycode == SYM_F || keycode == SYM_J) ? FLOW_TAP_TERM_INDEX_SHIFT : FLOW_TAP_TERM;
}

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [L_BASE] = LAYOUT(
        KC_PLUS, KC_1, KC_2, KC_3, KC_4, KC_5,                          KC_6, KC_7, KC_8, KC_9, KC_0, KC_MINS,
        KC_TAB, KC_Q, KC_W, KC_E, KC_R, KC_T,                           KC_Y, KC_U, KC_I, KC_O, KC_P, KC_BSLS,
        KC_ESC, CTL_A, OPT_S, CMD_D, SYM_F, KC_G,                       KC_H, SYM_J, CMD_K, OPT_L, CTL_SCLN, KC_QUOT,
        MO(L_MAGIC), KC_Z, KC_X, KC_C, KC_V, KC_B,                      KC_N, KC_M, KC_COMM, KC_DOT, KC_SLSH, CW_TOGG,
                                      LT(L_CURSOR, KC_BSPC), KC_LSFT, KC_NO, KC_ENTER, LT(L_NUM, KC_SPACE),
                                      KC_NO, KC_NO, KC_NO
    ),
    [L_SYM] = LAYOUT(
        _______, KC_GRV, KC_LABK, KC_RABK, KC_MINS, KC_PIPE,             KC_CIRC, KC_LCBR, KC_RCBR, KC_DLR, ARROW, _______,
        _______, _______, _______, _______, _______, _______,            _______, _______, _______, _______, _______, _______,
        _______, KC_EXLM, KC_ASTR, KC_SLSH, KC_EQL, KC_AMPR,             KC_HASH, KC_LPRN, KC_RPRN, KC_SCLN, KC_DQUO, _______,
        _______, KC_TILD, KC_PLUS, KC_LBRC, KC_RBRC, KC_PERC,             KC_AT, KC_COLN, KC_QUOT, KC_UNDS, KC_QUES, _______,
                                      _______, _______, _______, _______, _______,
                                      _______, _______, _______
    ),
    [L_CURSOR] = LAYOUT(
        _______, _______, LCMD(KC_R), LCTL(LSFT(KC_TAB)), LCTL(KC_TAB), LCMD(KC_LBRC),   LCMD(KC_RBRC), KC_PGUP, KC_HOME, KC_UP, KC_END, SRCHSEL,
        _______, _______, _______, _______, _______, _______,                                KC_PGDN, KC_LEFT, KC_DOWN, KC_RIGHT, _______, _______,
        _______, KC_LCTL, KC_LALT, KC_LGUI, KC_LSFT, MS_BTN1,                                _______, KC_LEFT, KC_DOWN, KC_RIGHT, _______, _______,
        _______, LCMD(KC_Z), LCMD(LSFT(KC_Z)), LCMD(KC_C), LCMD(KC_V), LCMD(LSFT(KC_V)),       LCMD(KC_L), SELWBAK, SELWORD, SELLINE, _______, _______,
                                      _______, _______, _______, _______, _______,
                                      _______, LCMD(KC_TAB), QK_LLCK
    ),
    [L_NUM] = LAYOUT(
        KC_ESC, KC_F1, KC_F2, KC_F3, KC_F4, KC_F5,                     KC_F6, KC_F7, KC_F8, KC_F9, KC_F10, KC_F11,
        _______, KC_SLSH, KC_9, KC_8, KC_7, KC_ASTR,                   _______, _______, KC_LBRC, KC_RBRC, _______, KC_F12,
        _______, KC_MINS, KC_3, KC_2, KC_1, KC_PLUS,                   _______, KC_RSFT, KC_RGUI, KC_RALT, KC_RCTL, _______,
        _______, KC_X, KC_6, KC_5, KC_4, KC_PERC,                     _______, _______, KC_COMM, KC_DOT, _______, _______,
                                      KC_0, _______, _______, _______, _______,
                                      _______, QK_LLCK, _______
    ),
    [L_MAGIC] = LAYOUT(
        _______, RM_TOGG, QK_KB, RM_NEXT, RGB_SLD, RM_VALD,             RM_VALU, HSV_0_0_255, HSV_0_255_255, HSV_74_255_255, HSV_169_255_255, _______,
        _______, KC_MEDIA_PREV_TRACK, KC_MEDIA_NEXT_TRACK, KC_MEDIA_STOP, KC_MEDIA_PLAY_PAUSE, _______,   _______, _______, _______, _______, _______, _______,
        _______, KC_AUDIO_VOL_DOWN, KC_AUDIO_VOL_UP, KC_AUDIO_MUTE, _______, _______,             _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,             _______, _______, _______, _______, _______, QK_BOOT,
                                      _______, _______, _______, _______, _______,
                                      _______, _______, _______
    ),
};

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    if (!record->event.pressed) return true;
    switch (keycode) {
        case ARROW: {
            const uint8_t mods = get_mods() | get_weak_mods();
            const bool shifted = mods & MOD_MASK_SHIFT;
            const bool alted = mods & MOD_MASK_ALT;
            clear_mods(); clear_weak_mods();
            send_string(alted ? (shifted ? "<=>" : "<->") : (shifted ? "=>" : "->"));
            set_mods(mods);
            return false;
        }
        case SRCHSEL:
            tap_code16(LCMD(KC_C)); wait_ms(50); tap_code16(LCMD(KC_T)); wait_ms(50); tap_code16(LCMD(KC_V)); tap_code(KC_ENTER); return false;
        case RGB_SLD: rgb_matrix_mode(RGB_MATRIX_SOLID_COLOR); return false;
        case HSV_0_0_255: rgb_matrix_mode(RGB_MATRIX_SOLID_COLOR); rgb_matrix_sethsv(0, 0, 255); return false;
        case HSV_0_255_255: rgb_matrix_mode(RGB_MATRIX_SOLID_COLOR); rgb_matrix_sethsv(0, 255, 255); return false;
        case HSV_74_255_255: rgb_matrix_mode(RGB_MATRIX_SOLID_COLOR); rgb_matrix_sethsv(74, 255, 255); return false;
        case HSV_169_255_255: rgb_matrix_mode(RGB_MATRIX_SOLID_COLOR); rgb_matrix_sethsv(169, 255, 255); return false;
    }
    return true;
}
