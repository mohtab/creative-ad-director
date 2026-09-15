#!/usr/bin/env python3
"""Validate an ad edit plan, not rendered media. Uses only Python stdlib.

Usage: python3 validate_timeline.py manifest.json
       python3 validate_timeline.py --self-test
Times are seconds (not SMPTE timecode). Use strings for precise decimals.
All timing is editorial: no claim a generative model obeys these boundaries.
"""
import argparse
import copy
from fractions import Fraction
import json
from pathlib import Path
import re
import unittest


def number(value):
    if isinstance(value, bool):
        raise ValueError('Boolean is not a timing value')
    return Fraction(str(value))


def validate(plan):
    errors, warnings = [], []
    result = {'valid': False, 'errors': errors, 'warnings': warnings,
              'scope': 'edit-plan arithmetic only; render, continuity and spoken performance not verified'}
    try:
        duration = number(plan['duration_seconds'])
        fps = number(plan['fps'])
        if duration <= 0 or fps <= 0:
            raise ValueError('Duration and fps must be positive')
        frames = duration * fps
        if frames.denominator != 1:
            errors.append('Total duration is not an integer number of frames')
        result['total_frames'] = int(frames) if frames.denominator == 1 else str(frames)
        shots = plan['shots']
        if not isinstance(shots, list) or not shots:
            raise ValueError('At least one shot is required')
        result['shot_count'] = len(shots)
        previous_end = Fraction(0)
        shot_frames, boundaries = [], [Fraction(0)]
        for index, shot in enumerate(shots, 1):
            if shot['id'] != index:
                errors.append(f'Shot {index}: IDs must be consecutive starting at 1')
            start, end = number(shot['start']), number(shot['end'])
            if start != previous_end:
                errors.append(f'Shot {index}: gap, overlap or incorrect start')
            if start < 0 or end <= start or end > duration:
                errors.append(f'Shot {index}: invalid or out-of-range window')
            if (start * fps).denominator != 1 or (end * fps).denominator != 1:
                errors.append(f'Shot {index}: boundary falls between frames')
            length = (end - start) * fps
            shot_frames.append(int(length) if length.denominator == 1 else str(length))
            boundaries.append(end)
            previous_end = end
        if previous_end != duration:
            errors.append('Final shot does not end at the target duration')
        result['shot_frames'] = shot_frames
        if 'bpm' in plan:
            bpm = number(plan['bpm'])
            if bpm <= 0:
                raise ValueError('BPM must be positive')
            beat = Fraction(60) / bpm
            beats_per_bar = number(plan.get('beats_per_bar', 4))
            if beats_per_bar <= 0:
                raise ValueError('Beats per bar must be positive')
            result['beat_seconds'] = float(beat)
            result['beats'] = float(duration / beat)
            result['bars'] = float(duration / beat / beats_per_bar)
            off_grid = [str(t) for t in boundaries if (t / beat).denominator != 1]
            result['all_cuts_on_beats'] = not off_grid
            if off_grid and plan.get('require_beat_grid', False):
                errors.append('Required beat grid violated at: ' + ', '.join(off_grid))
        voice_windows = []
        prior_voice_end = Fraction(0)
        for index, line in enumerate(plan.get('voiceover', []), 1):
            start, end = number(line['start']), number(line['end'])
            if start < 0 or end <= start or end > duration:
                errors.append(f'VO {index}: invalid or out-of-range window')
                continue
            if start < prior_voice_end:
                errors.append(f'VO {index}: overlaps previous line or is out of order')
            prior_voice_end = end
            text = line['text']
            if not isinstance(text, str) or not text.strip():
                errors.append(f'VO {index}: nonempty text required')
                continue
            words = len(re.findall(r"\S+", text))
            wpm = Fraction(words * 60) / (end - start)
            voice_windows.append({'line': index, 'whitespace_word_count': words,
                                  'estimated_wpm': round(float(wpm), 1)})
            if wpm > number(plan.get('voiceover_warning_wpm', 160)):
                warnings.append(f'VO {index}: estimated delivery exceeds chosen WPM warning threshold')
        if voice_windows:
            result['voiceover'] = voice_windows
            warnings.append('WPM uses whitespace-delimited words; language, pauses and performance require a spoken check')
        for index, title in enumerate(plan.get('titles', []), 1):
            start, full, end = map(number, (title['start'], title['fully_visible'], title['end']))
            if not (0 <= start <= full < end <= duration):
                errors.append(f'Title {index}: invalid fade/hold window')
            if any((t * fps).denominator != 1 for t in (start, full, end)):
                errors.append(f'Title {index}: boundary falls between frames')
            if end - full < number(title.get('minimum_hold_seconds', 0)):
                warnings.append(f'Title {index}: full-opacity hold shorter than requested minimum')
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        errors.append(f'Invalid manifest: {exc}')
    result['valid'] = not errors
    return result


class TimelineTests(unittest.TestCase):
    def base(self):
        return {'duration_seconds': 3, 'fps': 24, 'bpm': 80,
                'require_beat_grid': True,
                'shots': [{'id': 1, 'start': 0, 'end': 1.5},
                          {'id': 2, 'start': 1.5, 'end': 3}]}

    def test_valid(self):
        result = validate(self.base())
        self.assertTrue(result['valid'])
        self.assertEqual(result['total_frames'], 72)
        self.assertEqual(result['shot_frames'], [36, 36])

    def test_gap(self):
        plan = self.base(); plan['shots'][1]['start'] = 2
        self.assertFalse(validate(plan)['valid'])

    def test_overlap(self):
        plan = self.base(); plan['shots'][1]['start'] = 1
        self.assertFalse(validate(plan)['valid'])

    def test_fractional_frame(self):
        plan = self.base(); plan['shots'][0]['end'] = '1.51'
        plan['shots'][1]['start'] = '1.51'
        self.assertFalse(validate(plan)['valid'])

    def test_wrong_end(self):
        plan = self.base(); plan['shots'][1]['end'] = '2.25'
        self.assertFalse(validate(plan)['valid'])

    def test_off_beat_but_frame_aligned(self):
        plan = self.base(); plan['shots'][0]['end'] = '1.625'
        plan['shots'][1]['start'] = '1.625'
        self.assertFalse(validate(plan)['valid'])
        plan['require_beat_grid'] = False
        self.assertTrue(validate(plan)['valid'])

    def test_voice_out_of_range(self):
        plan = self.base(); plan['voiceover'] = [{'start': 2, 'end': 4, 'text': 'Test line'}]
        self.assertFalse(validate(plan)['valid'])

    def test_invalid_fps(self):
        plan = self.base(); plan['fps'] = 0
        self.assertFalse(validate(plan)['valid'])

    def test_invalid_title(self):
        plan = self.base(); plan['titles'] = [{'start': 2, 'fully_visible': 1, 'end': 3}]
        self.assertFalse(validate(plan)['valid'])

    def test_fast_voice_warns(self):
        plan = self.base(); plan['voiceover'] = [{'start': 0, 'end': 1, 'text': 'This line has too many words for one second'}]
        result = validate(plan)
        self.assertTrue(result['valid'])
        self.assertTrue(any('threshold' in item for item in result['warnings']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', nargs='?', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TimelineTests)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        raise SystemExit(0 if result.wasSuccessful() else 1)
    if args.manifest is None:
        parser.error('A manifest or --self-test is required')
    result = validate(json.loads(args.manifest.read_text()))
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['valid'] else 1)
