from __future__ import print_function

from pyteomics import biolccc

import click

@click.group()
def main():
    pass

@main.command()
def chemGroups():
    for label, chemicalGroup in biolccc.rpAcnFaRod['chemicalGroups'].items():
        print('Name', chemicalGroup['name'])
        print('Label', chemicalGroup['label'])
        print('Binding energy', chemicalGroup['bindEnergy'])
        print('Average mass', chemicalGroup['averageMass'])
        print('Monoisotopic mass', chemicalGroup['monoisotopicMass'])


@main.command()
@click.option('--column-length', default=100.0, show_default=True,
              help='the column length in mm')
@click.option('--diameter', default=0.1, show_default=True,
              help='the internal column diameter in mm')
@click.option('--pore-size', default=300.0, show_default=True,
              help='average pore size in Angstroms')
@click.option('--concA', default=5.0, show_default=True,
              help='Concentration (%) of the eluting solvent (ACN for reverse phase) of component A')
@click.option('--concB', default=95, show_default=True,
              help='Concentration (%) of the eluting solvent (ACN for reverse phase) of component B')
@click.option('--flow-rate', default=0.0005,  show_default=True,
             help='flow rate in mL/min')
@click.option('--gradientStart', default=0.0, show_default=True,
             help='Gradient start percent B')
@click.option('--gradientStop', default=90.0, show_default=True,
             help='Gradient stop percent B')
@click.option('--gradientLength', default=60.0, show_default=True,
             help='Gradient length in minutes')
@click.option('--input-type', type=click.Choice(['string', 'file']), default='string',
              show_default=True, help='Whether or not the input is a string of peptides or files of peptides')
@click.argument('peptide', nargs=-1)
def run(column_length, diameter, pore_size, conca, concb, flow_rate,
        gradientstart, gradientstop, gradientlength, input_type, peptide):
    """See biolccc documentation"""

    if len(peptide) == 0:
        raise ValueError('Must supply at least 1 peptide')
    if input_type == 'file':
        peptide = [x for y in [open(x).read().split() for x in peptide] for x in y]


    chroma = biolccc.ChromoConditions()

    chroma['columnLength'] = column_length
    chroma['columnDiameter'] = diameter
    chroma['columnPoreSize'] = pore_size
    chroma['secondSolventConcentrationA'] = conca
    chroma['secondSolventConcentrationB'] = concb
    chroma['gradient'] = biolccc.Gradient(gradientstart, gradientstop, gradientlength)
    chroma['flowRate'] = flow_rate

    results = dict()
    for p in peptide:
        RT = biolccc.calculateRT(str(p),
                                 biolccc.rpAcnFaRod,
                                 chroma
        )
        results[p] = RT


    print('Peptide', '\t', 'RTmin')
    for p, rt in results.items():
        print(p, '\t', rt)

if __name__ == '__main__':
    main()
