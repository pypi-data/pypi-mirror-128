import json
from .text_tracker import TextTracker

class TextConfigGenerator:

    def __init__(self, default_ocr_config=None):
        # only used for exluding from pairs
        self.labels_to_track = set()
        self.tracking_configurations = {}
        self.default_ocr_config = default_ocr_config

    def add_label_to_configuration(self, images, label_to_track, ocr_rect, other_ocr_rects=None, true_label=None, source_group=None, assisted_label_rect=None, ignore_if_labels_exists=None, ignore_if_regex_triggered=None, ignore_trigger_threshold=0.0, ignore_trigger_rects=None,
                override_rect_threshold=0.0, override_rects=None, ocr_config=None, other_ocr_configs=None, frames_to_skip=None, override_style=None):

        if true_label is None:
            true_label = label_to_track

        # true labels only. secondaries not included.
        self.labels_to_track.add(label_to_track)
        config = {
            "label": true_label,
            "position": "fixed",
            "ocr_rect": ocr_rect,
        }

        if frames_to_skip is None:
            frames_to_skip = 0

        if override_style in [None, 'base_style', 'custom']:
            config['override_style'] = override_style
        else:
            config['override_style'] = None

        config['frames_to_skip'] = frames_to_skip

        if other_ocr_rects is not None:
            config['other_ocr_rects'] = other_ocr_rects

        if assisted_label_rect is not None:
            config['assisted_label_rect'] = assisted_label_rect

        # add
        if source_group is not None:
            config['source_group'] = source_group

        if ignore_if_labels_exists is not None:
            config['ignore_if_labels_exists'] = ignore_if_labels_exists

        if ignore_if_regex_triggered is not None:
            config['ignore_if_regex_triggered'] = ignore_if_regex_triggered

        if ignore_trigger_rects is not None:
            ignore_config = {}
            ignore_config['rects'] = TextTracker.get_min_max_colors_for_regions_in_images(images, ignore_trigger_rects)
            ignore_config['threshold'] = ignore_trigger_threshold
            config['ignore_trigger_rects'] = ignore_config


        if override_rects is not None:
            config['override_rects'] = TextTracker.get_min_max_colors_for_regions_in_images(images, override_rects)
            config['threshold'] = ignore_trigger_threshold

        if ocr_config is not None:
            config['ocr_config'] = ocr_config
        elif self.default_ocr_config is not None:
            config['ocr_config'] = self.default_ocr_config

        if other_ocr_configs is not None:
            config['other_ocr_configs'] = other_ocr_configs

        self.tracking_configurations[label_to_track] = config

    def get_generated_config(self):
        return {
            "labels_to_track": list(self.labels_to_track),
            "tracking_configurations": self.tracking_configurations,
        }

    def get_generated_config_as_json(self):
        return json.dumps(self.get_generated_config(), indent=4)
