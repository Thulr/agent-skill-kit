"""Level 2 Subroutine Compiler template.

Use for bounded, stateless text-in/text-out tasks: parsers, classifiers,
routers, linter triagers, multi-hop query generators. Compiles a declarative
signature into an optimized predictor against a metric and a small training
set.

CI parses this with `python3 -m py_compile`; the `dspy` import is NOT
executed in the sandbox. The skill copies this file into the host
workspace's `ai-ops/` directory when a Level 2 scaffold is selected.

Default optimizer is BootstrapFewShot with max_bootstrapped_demos=1, which
tolerates small (5-10 example) training sets. For real compilation, supply
at least 50 examples and switch to MIPROv2.
"""
import dspy
from dspy.teleprompt import BootstrapFewShot, MIPROv2  # noqa: F401


# 1. Define the Cognitive Subroutine (Signature)
class LinterTriage(dspy.Signature):
    """Analyze compiler/linter outputs and identify the files containing the root-cause bug."""

    linter_log: str = dspy.InputField(
        desc="Raw terminal output from compiler, linter, or test runner"
    )
    modified_files: list[str] = dspy.InputField(
        desc="List of files edited in this session"
    )
    target_files: list[str] = dspy.OutputField(
        desc="JSON array of file paths containing the root cause"
    )


# 2. Build the Module
class LinterTriager(dspy.Module):
    def __init__(self):
        super().__init__()
        self.triage = dspy.Predict(LinterTriage)

    def forward(self, linter_log, modified_files):
        return self.triage(linter_log=linter_log, modified_files=modified_files)


# 3. Define the Success Metric
def exact_match_metric(gold, pred, trace=None):
    return set(gold.target_files) == set(pred.target_files)


# 4. Compile the Module against your dataset
def compile_system():
    lm = dspy.LM("openai/gpt-4o-mini")
    dspy.configure(lm=lm)

    trainset = [
        dspy.Example(
            linter_log="TypeError: Cannot read properties of undefined (reading 'map') at App.tsx:12",
            modified_files=["src/App.tsx", "src/components/Header.tsx"],
            target_files=["src/App.tsx"],
        ).with_inputs("linter_log", "modified_files")
    ]

    optimizer = BootstrapFewShot(metric=exact_match_metric, max_bootstrapped_demos=1)

    print("Compiling cognitive subroutine...")
    compiled_triager = optimizer.compile(LinterTriager(), trainset=trainset)

    compiled_triager.save("ai-ops/compiled_triager.json")
    print("Subroutine successfully compiled to ai-ops/compiled_triager.json")


if __name__ == "__main__":
    compile_system()
