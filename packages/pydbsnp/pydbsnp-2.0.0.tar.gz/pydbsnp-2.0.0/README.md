# pydbsnp

Interface with dbSNP VCF data

## Installation

**Step 0 (optional):** If you don't want to bother with environment variables
and don't care about how `pydbsnp` works under the hood, skip this step.

If you wish, you can determine the location where `pydbsnp` looks for relevant
data using four environment variables: `PYDBSNP_VCF_GRCH37`,
`PYDBSNP_RSID_GRCH37`, `PYDBSNP_VCF_GRCH38`, `PYDBSNP_RSID_GRCH38`. The `VCF`
variables determine the location of the VCF data, the `RSID` variables
determine the location of the rsid indices. For example, you could add this
to your `.bash_profile`:

```bash
export PYDBSNP_VCF_GRCH37=<path of your choice>
export PYDBSNP_RSID_GRCH37=<path of your choice>
export PYDBSNP_VCF_GRCH38=<path of your choice>
export PYDBSNP_RSID_GRCH38=<path of your choice>
```

If you set these variables before continuing to the next step, `pydbsnp` will
use them to determine where it places downloaded VCF files and RSID indices.

**Step 1:** install the python package via `pip3`

```sh
pip install pydbsnp
```
or
```sh
pip install --user pydbsnp
```

**Step 2:** Once the python package is installed, download and index the dbSBP
VCF data:

```sh
pydbsnp-download
pydbsnp-index
```

For hg19/GRCh37 coordinates:

```sh
pydbsnp-download --reference-build GRCh37
pydbsnp-index
```

## Command line usage

```sh
pydbsnp-query -h
```

```sh
pydbsnp-query rs231361
pydbsnp-query chr8:118184783
pydbsnp-query --reference-build GRCh37 rs231361
pydbsnp-query rs231361 chr8:118184783 rs7903146
```

## API

Two classes are provided: `Variant` and `GeneralizedVariant`.

An object of the `Variant` class has an attribute for each relevant field
of the VCF.
```python
from pydbsnp import Variant
v = Variant(id='rs8056814')
print(v.chrom, v.pos, v.id, v.ref, v.alt)
print(v.info)
w = Variant(id='rs8056814', reference_build='GRCh37')
print(w.chrom, w.pos)
x = Variant('chr16', 75218429)
print(x)
help(Variant)
```

An object of the `GeneralizedVariant` class is similar, but each attribute
is a tuple which may have multiple items. For example, one RSID may map
to two sets of coordinates.
```python
gv = GeneralizedVariant(id='rs8056814')
print(gv.chrom, gv.pos, gv.id, gv.ref, gv.alt)
```
