import hashlib
import json
from io import BytesIO
from pathlib import Path
from typing import Optional, List, Union, NamedTuple, Dict, Any
from abc import ABC, abstractmethod
from collections.abc import Iterable
import subprocess
import shlex
from matchms import Spectrum
from .settings import Settings
from .matchms import load_from_cfm_id
from .hash import hash_file, hash_stream

ParamsPath = NamedTuple("ParamsPath", (("param", Path), ("conf", Path)))
PROB_THRESH_FOR_PRUNE_DEFAULT: float = 0.001


class CfmIdBase(ABC):
    params: Dict[str, Any]
    predict_hash: str
    prob_thresh_for_prune: float
    settings: Settings
    _PATH_ENV_KEY: str

    def __init__(
        self,
        cfm_id_cmd: Optional[str] = None,
        param: List[str] = ["param_output.log"],
        conf: List[str] = ["param_config.txt"],
        prob_thresh_for_prune: float = PROB_THRESH_FOR_PRUNE_DEFAULT,
    ):
        self.settings = Settings()
        self.set_cfm_id_path(cfm_id_cmd)
        self.param_path = Path(*param)
        self.conf_path = Path(*conf)
        self.prob_thresh_for_prune = prob_thresh_for_prune
        self.set_predict_hash()

    def set_cfm_id_path(self, cfm_id_cmd: Optional[str]) -> None:
        cfm_id_cmd = cfm_id_cmd or getattr(self.settings, self._PATH_ENV_KEY)
        if cfm_id_cmd is None:
            raise AttributeError(
                "Must provide cfm_id_cmd attribute or set environment variable"
            )
        self.cfm_id_cmd = cfm_id_cmd

    @abstractmethod
    def get_cmd(self, name: str) -> str:
        """
        Args:
            name: name of command to execute such as 'cfm-predict'
        Returns:
            Path to execute cfm-id command
        """

    @abstractmethod
    def get_params(self) -> ParamsPath:
        """
        Args:
            name: name of command to execute such as 'cfm-predict'
        Returns:
            Path to execute cfm-id command
        """

    @abstractmethod
    def set_params(self) -> None:
        """set self.params"""

    def set_predict_hash(self) -> None:
        """set self.params"""
        self.set_params()
        predict_params = {
            **self.params,
            "prob_thresh_for_prune": self.prob_thresh_for_prune,
        }
        self.predict_hash = hashlib.md5(
            json.dumps(predict_params, sort_keys=True).encode()
        ).hexdigest()

    def predict(
        self,
        smiles: Union[str, List[str]],
        include_annotations: bool = False,
        raw_format: bool = False,
    ) -> Union[str, List[Spectrum]]:
        if isinstance(smiles, str):
            return self._predict_single(
                smiles, self.prob_thresh_for_prune, include_annotations, raw_format
            )
        elif isinstance(smiles, Iterable):
            if raw_format:
                raise AttributeError(
                    "Raw format option is available only for single smiles"
                )
            spectra: List[Spectrum] = []
            for sm in smiles:
                spectra += self._predict_single(
                    sm,
                    self.prob_thresh_for_prune,
                    include_annotations,
                    raw_format=False,
                )
            return spectra
        else:
            raise AttributeError("smiles must be a str or an iterable of str")

    def _predict_single(
        self,
        smiles: str,
        prob_thresh_for_prune: float,
        include_annotations: bool,
        raw_format: bool,
    ) -> Union[str, List[Spectrum]]:
        raw_text = self._predict_raw_text(
            smiles, prob_thresh_for_prune, include_annotations
        )
        metadata = {"smiles": smiles, "cfm_predict_hash": self.predict_hash}
        if raw_format:
            return raw_text
        spectra = load_from_cfm_id(raw_text, metadata=metadata)
        return spectra

    def _predict_raw_text(
        self, smiles: str, prob_thresh_for_prune: float, include_annotations: bool
    ) -> str:
        bin_path = self.get_cmd("cfm-predict")
        cmd_ = (
            *shlex.split(str(bin_path)),
            smiles,
            prob_thresh_for_prune,
            *self.get_params(),
            int(include_annotations),
        )
        cmd = [str(arg) for arg in cmd_]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, _ = process.communicate()
        return stdout.decode()


class CfmId(CfmIdBase):
    _PATH_ENV_KEY = "CFMID_PATH"

    def get_cmd(self, name: str) -> str:
        return str(Path(self.cfm_id_cmd, name))

    def get_params(self) -> ParamsPath:
        return ParamsPath(
            Path(self.cfm_id_cmd) / self.param_path,
            Path(self.cfm_id_cmd) / self.conf_path,
        )

    def set_params(self) -> None:
        params = self.get_params()
        self.params = {
            "param": hash_file(params.param),
            "conf": hash_file(params.conf),
        }


class CfmIdDocker(CfmIdBase):
    _PATH_ENV_KEY = "CFMID_IMAGE"

    def get_cmd(self, name: str) -> str:
        return f"docker run {self.cfm_id_cmd} {name}"

    def get_params(self) -> ParamsPath:
        return ParamsPath(self.param_path, self.conf_path)

    def set_params(self) -> None:
        params = self.get_params()
        self.params = {
            key: hash_stream(self._get_docker_file(str(param)))
            for key, param in zip(("param", "conf"), params)
        }

    def _get_docker_file(self, file_name: str) -> BytesIO:
        cmd = [*shlex.split(f"docker run {self.cfm_id_cmd}"), "cat", file_name]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, _ = process.communicate()
        return BytesIO(stdout)


class CfmIdTCP(CfmIdBase):
    _PATH_ENV_KEY = "CFMID_HOST"
    params_dir: Optional[Path] = None

    def get_cmd(self, name: str) -> str:
        return f"netcat {self.cfm_id_cmd} {self.settings.CFMID_PORT}"

    def get_params(self) -> ParamsPath:
        param_dir = self.params_dir or Path()
        return ParamsPath(
            param_dir / self.param_path,
            param_dir / self.conf_path,
        )

    def set_params(self) -> None:
        if self.params_dir:
            params = self.get_params()
            self.params = {
                "param": hash_file(params.param),
                "conf": hash_file(params.conf),
            }
        else:
            self.params = {}

    def _predict_raw_text(
        self, smiles: str, prob_thresh_for_prune: float, include_annotations: bool
    ) -> str:
        bin_path = self.get_cmd("cfm-predict")
        p1 = subprocess.Popen(["echo", "cfm-predict", smiles], stdout=subprocess.PIPE)
        process = subprocess.Popen(
            shlex.split(str(bin_path)),
            stdin=p1.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, _ = process.communicate()

        return stdout.decode()
