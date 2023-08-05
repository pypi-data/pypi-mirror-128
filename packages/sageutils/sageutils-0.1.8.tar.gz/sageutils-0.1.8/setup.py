from src.sageutils import __version__
from setuptools import find_packages, setup

long_description = """# sageutils
Common utility functions

https://github.com/ttong-ai/sageutils/blob/main/README.md

Supported Python version: 3.8.0+

### Install dependencies:
Make sure you install to the correct Python environment.
`pip install -r requirements.txt` or `pip3 install -r requirements.txt`


### passutils.py

`permutate` and `reverse_permutate` use SHA256 to cryptographically add puseudorandom permutation to the mnemonic pass phrases commonly seen in the crypto world.

If the mnemonic pass phrase is `one two three four five six seven eight nine ten`, you can randomize it by adding an easy-to-remember personal `key`.  In the following example, if the `key` is `disney`, the randomized pass phrase would be `one four ten five eight three six seven two nine`. You can store this permutated version of passphrase in your cloud-based password managers. Even if a bad actor somehow hacked your password manager and stole your randomized private key phrase due to security breach, it would be almost impossible for the bad actor to figure out the correct sequence to your private pass phrase. You will have precious time to move your funds to newly secured locations. (It is still important to keep best security practices for your password managers!) 

When you need to use your private pass phrase, just use the `reverse_permutate` command with the same personal `key`. This can be generated only when you need to use the private pass phrase. But do not store it anywhere!! 

You do need to always remember your personal `key`, this is your responsibility. Use a simple word that you and trusted ones would always remember. If you forget your personal `key`, the original sequence of the pass phrase may be permenantly lost.  

Command line usage:

```Python
passutil permutate "one two three four five six seven eight nine ten" --key="disney"

Output with encrypted permutation:
eight seven four nine three five two ten one six
```

```Python
passutils reverse-permutate "eight seven four nine three five two ten one six" --key="disney"

Output of original sequence:
one two three four five six seven eight nine ten
```

## Disclaimer
The password utiltiy functions are provided as is. We are not responsible for any losses due to misuses or forgotten personal key or any bugs. You will need to test it and feel comfortable with the process before using it.
"""


setup(
    name="sageutils",
    packages=find_packages(),
    scripts=["scripts/passutil"],
    version=__version__,
    description="Sage common utilities library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tony Tong",
    author_email="ttong@pro-ai.org",
    license="MIT",
    python_requires=">=3.6, <4.0",
    include_package_data=True,
    install_requires=[
        "cryptography",
        "fire",
    ],
)
