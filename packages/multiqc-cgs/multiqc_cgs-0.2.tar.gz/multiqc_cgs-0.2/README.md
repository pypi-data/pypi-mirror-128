# MultiQC plugin: customize general statistics

```
# install module in same environment as multiqc
git push origin master
```

## Example

```
# Add the following entry to your multiqc config
# This example add picard metrics PF_READS_ALIGNED
# all fields used by multiqc, for example title, can be set
multiqc_cgs:
  Picard:
    PF_READS_ALIGNED:
      title: "M Aligned reads"
      description: "Number of million reads in bam from Picard"
      format: "{:.1f}"
      shared_key: "read_count"

``
