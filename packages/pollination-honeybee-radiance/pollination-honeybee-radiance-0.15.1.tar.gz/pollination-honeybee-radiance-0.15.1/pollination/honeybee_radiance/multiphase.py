from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class ViewMatrix(Function):
    """Calculate view matrix for a receiver file."""

    radiance_parameters = Inputs.str(
        description='Radiance parameters. -I, -c 1 and -aa 0 are already included in '
        'the command.', default=''
    )

    fixed_radiance_parameters = Inputs.str(
        description='Radiance parameters. -I, -c 1 and -aa 0 are already included in '
        'the command.', default='-aa 0'
    )

    sensor_count = Inputs.int(
        description='Number of maximum sensors in each generated grid.',
        spec={'type': 'integer', 'minimum': 1}
    )

    receiver_file = Inputs.file(
        description='Path to a receiver file.', path='receiver.rad',
        extensions=['rad']
    )

    sensor_grid = Inputs.file(
        description='Path to sensor grid files.', path='grid.pts',
        extensions=['pts']
    )

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct',
        extensions=['oct']
    )

    receivers_folder = Inputs.folder(
        description='Folder containing any receiver files needed for ray tracing.',
        path='receivers'
    )

    bsdf_folder = Inputs.folder(
        description='Folder containing any BSDF files needed for ray tracing.',
        path='model/bsdf', optional=True
    )

    @command
    def run_view_mtx(self):
        return 'honeybee-radiance multi-phase view-matrix receiver.rad scene.oct ' \
            'grid.pts --sensor-count {{self.sensor_count}} --output output.vmx ' \
            '--rad-params "{{self.radiance_parameters}}" --rad-params-locked '\
            '"{{self.fixed_radiance_parameters}}"'

    view_mtx = Outputs.file(
        description='Output view matrix file.', path='output.vmx'
    )
