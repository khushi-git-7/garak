"""pytest plugin (fork-only sweep): log every test where Attempt.outputs_for(lang) drops outputs the attempt has."""
import os
import garak.attempt as A

_orig = A.Attempt.outputs_for
LOG = os.path.abspath("sweep.log")


def outputs_for(self, lang):
    got = _orig(self, lang)
    if len(got) < len(self.outputs):
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"{os.environ.get('PYTEST_CURRENT_TEST', '?').split(' ')[0]}\tlang_spec={lang!r}\tprompt_lang="
                    f"{getattr(self.prompt.last_message(), 'lang', None)!r}\t{len(got)} of {len(self.outputs)}\n")
    return got


A.Attempt.outputs_for = outputs_for
