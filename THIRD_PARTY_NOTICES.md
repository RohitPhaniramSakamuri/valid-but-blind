# Third-party rights and attribution

The repository's [all-rights-reserved notice](LICENSE) covers only original material owned by Rohit Phaniram Sakamuri. It does not relicense third-party material or claim ownership of existing algorithms, scientific methods, facts, datasets or architectures. Third-party rights and existing permissions remain in force.

## Model architecture code

The following model architecture files were obtained from or derived from the RobustBench model implementations. The upstream benchmark code is MIT-licensed; its complete upstream license notice, including the separate model-weight notices, is preserved in [LICENSES/RobustBench.txt](LICENSES/RobustBench.txt).

- `demo/arch_wide_resnet.py`
- `diagnostics/2026-11-01-exp004-models/arch_wide_resnet.py` and `arch_resnet.py`
- `diagnostics/2026-11-03-exp006-confirm/job/arch_wide_resnet.py` and `arch_resnet.py`
- `diagnostics/2026-11-03-exp008-confirm/job/arch_wide_resnet.py` and `arch_resnet.py`
- `diagnostics/2026-11-14-exp010-confirm/job/arch_wide_resnet.py` and `arch_resnet.py`

The WideResNet implementation also identifies [TRADES](https://github.com/yaodongyu/TRADES) as an upstream source. Its MIT copyright and permission notice is preserved in [LICENSES/TRADES.txt](LICENSES/TRADES.txt). CIFAR ResNet implementations have an upstream lineage including [pytorch-cifar](https://github.com/kuangliu/pytorch-cifar); its MIT notice is preserved in [LICENSES/pytorch-cifar.txt](LICENSES/pytorch-cifar.txt). These notices also apply to corresponding upstream portions if copied into another local model wrapper. Original project-specific wrappers and experimental logic are covered by the root notice to the extent owned by the project author.

Upstream reference: [RobustBench](https://github.com/RobustBench/robustbench). Datasets and model weights are not redistributed in this repository; obtaining them does not change their respective terms.

## Manuscript formatting

`paper/llncs.cls` is the Springer LNCS document class. `paper/splncs04.bst` is a third-party bibliography style whose original copyright and LaTeX Project Public License notice remain in the file. These formatting files, including copies in the Overleaf archive, are excluded from the project's all-rights-reserved claim. Consult the retained notices and the [Springer author instructions](https://www.springer.com/gp/computer-science/lncs/conference-proceedings-guidelines) for the relevant distribution and use terms. The referenced LPPL text is included in [LICENSES/LPPL.txt](LICENSES/LPPL.txt).

The supplied `Review1.pptx`, `Review2.pptx` and `Review3.pptx` are assessment templates supplied to the project. No ownership of their pre-existing content or formatting is asserted. The authored research text, diagrams and result summaries in the completed review documents are distinct from those pre-existing templates.

## Published risk monitor

The project cites and evaluates [monasch/tta-monitor](https://github.com/monasch/tta-monitor), the released implementation of *Monitoring Risks in Test-Time Adaptation*. Its package is fetched separately and is not vendored here. Consult the upstream repository and retained notices for its applicable terms; no additional permission for its code is assumed or granted by this project. Loader patches in the diagnostic folders identify the project-specific calibration change. The root notice does not assert ownership of any upstream context or code portions in those patches or of the original authors' implementation.

## Libraries, literature and data

PyTorch, torchvision, NumPy, SciPy, scikit-learn, confseq, LightGBM, python-pptx, python-docx, LibreOffice and other external packages retain their own licenses. Referencing, downloading or importing them does not place them under the root rights notice.

CIFAR corruption datasets, MedMNIST datasets, published checkpoints and cited papers retain their respective owners' rights. Their inclusion in a bibliography or use in an experiment is not a claim of authorship or a new permission to redistribute them. Downloaded third-party papers, datasets and model weights are excluded from this public repository.
