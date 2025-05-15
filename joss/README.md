# JOSS template


Statement of need
   Area of need
Related Software
Related Research
Availability, Development, and Documentation


Summary: Has a clear description of the high-level functionality and purpose of the software for a diverse, non-specialist audience been provided?

A statement of need: Does the paper have a section titled ‘Statement of need’ that clearly states what problems the software is designed to solve, who the target audience is, and its relation to other work?

- The authors should clearly state what problems the software is designed to solve, who the target audience is, and its relation to other work.

Example usage
The authors should include examples of how to use the software (ideally to solve real-world analysis problems).

API documentation
Reviewers should check that the software API is documented to a suitable level.

Good: All functions/methods are documented including example inputs and outputs
OK: Core API functionality is documented
Bad (not acceptable): API is undocumented

Community guidelines
There should be clear guidelines for third-parties wishing to:

Contribute to the software

Report issues or problems with the software

Seek support



State of the field: Do the authors describe how this software compares to other commonly-used packages?

Quality of writing: Is the paper well written (i.e., it does not require editing for structure, language, or writing quality)?

References: Is the list of references complete, and is everything cited appropriately that should be cited (e.g., papers, datasets, software)? Do references in the text use the proper citation syntax?

 250-1000 words


# Comple

```
cd <ProjectDir>

docker run --rm \
    --volume $PWD/joss:/data \
    --user $(id -u):$(id -g) \
    --env JOURNAL=joss \
    openjournals/inara
```