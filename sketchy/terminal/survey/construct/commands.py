import click

from sketchy.utils import SketchySurvey
from pathlib import Path

DEFAULTS = {
    'kpneumoniae': dict(
        merge=dict(
            kleborate=dict(
                rmp=['rmpA', 'rmpA2']
            )
        ),
        config=dict(
            kleborate=[
                'ST',
                'virulence_score',
                'resistance_score',
                'Yersiniabactin',
                'K_locus',
                'O_locus',
                'AGly',
                'Col',
                'Fcyn',
                'Flq',
                'Gly',
                'MLS',
                'Ntmdz',
                'Phe',
                'Rif',
                'Sul',
                'Tet',
                'Tmt',
                'Bla',
                'Bla_Carb',
                'Bla_ESBL',
                'Bla_broad'
            ]
        ),
        binary=dict(
            kleborate=[
                'Yersiniabactin',
                'rmp',
                'AGly',
                'Col',
                'Fcyn',
                'Flq',
                'Gly',
                'MLS',
                'Ntmdz',
                'Phe',
                'Rif',
                'Sul',
                'Tet',
                'Tmt',
                'Bla',
                'Bla_Carb',
                'Bla_ESBL',
                'Bla_broad'
            ]
        )
    ),
    'saureus': dict(
        config=dict(
            sccion=[
                'mlst',
                'meca',
                'pvl',
                'spa',
                'scc'
            ],
            mykrobe_phenotype=[
                'Clindamycin',
                'Rifampicin',
                'Ciprofloxacin',
                'Vancomycin',
                'Tetracycline',
                'Mupirocin',
                'Gentamicin',
                'Trimethoprim',
                'Penicillin',
                'Methicillin',
                'Erythromycin',
                'FusidicAcid'
            ]
        ),
        merge=dict(),
        binary=dict()
    ),
    'mtuberculosis': dict(
        config=dict(
            mykrobe_phenotype=[
                'Clindamycin',
                'Rifampicin',
                'Ciprofloxacin',
                'Vancomycin',
                'Tetracycline',
                'Mupirocin',
                'Gentamicin',
                'Trimethoprim',
                'Penicillin',
                'Methicillin',
                'Erythromycin',
                'FusidicAcid'
            ],
            mykrobe_lineage=[
                'lineage'
            ]
        ),
        merge=dict(),
        binary=dict()
    ),
}


@click.command()
@click.option(
    '--directory', '-d', default=None, required=True, type=Path,
    help='Input directory with collected output from Pathfinder Survey'
)
@click.option(
    '--output', '-o', default='survey.tsv', type=Path,
    help='Tab-delimited genotype feature index for Sketchy'
)
@click.option(
    '--template', '-t', default=None, type=str,
    help='Use a configuration template: saureus, kpneumoniae, mtuberculosis'
)
@click.option(
    '--missing', '-m', default='-', type=str,
    help='Set a missing character [-]'
)
def construct(directory, output, template, missing):

    """ Construct genotype feature data from Pathfinder Survey """

    survey = SketchySurvey(
        survey_directory=directory
    )

    survey.missing = missing

    data = survey.construct(
        config=DEFAULTS[template]['config'],
        binary=DEFAULTS[template]['binary'],
        merge=DEFAULTS[template]['merge']
    )

    # All columns should be lower-case
    data.columns = [c.lower() for c in data.columns]

    data.to_csv(output, sep='\t', index_label='uuid')
