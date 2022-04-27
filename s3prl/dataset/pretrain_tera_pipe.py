from .common_pipes import (
    SetOutputKeys, 
    LoadAudio
)
from .extract_feat_pipes import ExtractKaldiFeat
from .noise_augmentation_pipes import NoiseAugmentation
from .masked_reconstruction_pipes import PrepareTargetFeat, MaskedReconstruction
from .base import SequentialDataPipe


class PretrainTaskPipe(SequentialDataPipe):
    """
    each item in the input dataset should have:
        wav_path: str
        label: str
    """

    def __init__(
        self,
        output_keys: dict = None,
        mask_args: dict = None,
        noise_args: dict = None,
        audio_config: dict = None,
        audio_sample_rate: int = 16000,
        audio_channel_reduction: str = "first",
        n_jobs: int = 6,
    ):
        output_keys = output_keys or dict(
            x="wav",
            x_len="wav_len",
            train_data="masked_data",
        )

        mask_args = mask_args or dict(
            position_encoding_size=768,    # int, this should be identical to `hidden_size`
            mask_proportion=0.15,          # float, mask this percentage of all spectrogram frames in each sequence at random during MAM training
            mask_consecutive_min=7,        # int, mask this amount of consecutive frames
            mask_consecutive_max=7,        # int, mask this amount of consecutive frames
            mask_allow_overlap=True,       # bool, allow overlap masking
            mask_bucket_ratio=1.5,         # float, only used when overlap is not allowed. sample a mask from each bucket in size of [sampled mask_consecutive * mask_bucket_ratio]
            mask_frequency=0,              # int, mask maximum this percentage of frequency bands, set to 0 for no frequency mask  
        )

        noise_args = noise_args or dict(
            noise_proportion=0.0,          # float, for this percentage of the time, Gaussian noise will be applied on all frames during MAM training, set to 0 for no noise
        )

        audio_config = audio_config or dict(
                kaldi = { 
                    "feat_type": "fbank",
                    "fbank": {
                            "frame_length": 25.0,
                            "frame_shift": 10.0,
                            "num_mel_bins": 80,
                            "use_log_fbank": True
                    },
                    "mfcc": {
                            "frame_length": 25.0,
                            "frame_shift": 10.0,
                            "num_ceps": 13
                    },
                    "spectrogram": {
                        "frame_length": 25.0, 
                        "frame_shift": 10.0
                    }
                },
                delta = {"order": 2, "win_length": 5},
                cmvn = {"use_cmvn": True},
        )

        super().__init__(
            LoadAudio(
                n_jobs=n_jobs,
                audio_sample_rate=audio_sample_rate,
                audio_channel_reduction=audio_channel_reduction,
            ),
            ExtractKaldiFeat(audio_config=audio_config, feat_name="source_feat"),
            PrepareTargetFeat(use_copy=True, 
                            source_feat_name="source_feat",
                            target_feat_name="target_feat"),
            NoiseAugmentation(noise_args=noise_args,
                            input_feat_name="source_feat",
                            output_feat_name="source_feat"),
            MaskedReconstruction(mask_args=mask_args, 
                                source_feat_name="source_feat",
                                target_feat_name="target_feat"),
            SetOutputKeys(output_keys=output_keys),
        )