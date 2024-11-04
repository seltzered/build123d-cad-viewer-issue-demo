# [Imports]
from build123d import *
from ocp_vscode import *

# [Parameters]
# Note: measurements based on looking at datasheet PDF
#       
#       ASIC/Connector params based on rough estimates from
#       datasheet drawings, not actual measurements
#

# step file from molex 781271210
connector_path = "./781271210.stp"

cirque_23mm_outer_dia = 23.20 * MM
cirque_23mm_pcb_plus_adhesive_thickness = 0.89 * MM

asic_length = 8.0 * MM
asic_width = 8.0 * MM
asic_y_center_offset = (5.6 * MM) - (asic_length / 2)
asic_thickness = 1.15 * MM

# connector_width = 8.3 * MM
connector_length = 3.1 * MM
connector_y_center_offset = (5.5 * MM) + (connector_length / 2) 
connector_thickness = 4.15 * MM

# [Code]
cirque_23mm_connector = import_step(connector_path)

with BuildPart() as cirque_23mm_pcb:
    with BuildSketch() as cirque_23mm_sk:
        Circle(cirque_23mm_outer_dia / 2.0)
    extrude(amount=cirque_23mm_pcb_plus_adhesive_thickness)

with BuildPart() as cirque_23mm_asic:
    with BuildSketch() as cirque_asic_sk:
        with Locations((0.0, asic_y_center_offset)):
            Rectangle(asic_length, asic_width)
    extrude(amount=(
        asic_thickness))

# with BuildPart() as cirque_23mm_connector:
#     with BuildSketch() as cirque_conn_sk:
#         with Locations((0.0, -connector_y_center_offset)):
#             Rectangle(connector_width, connector_length)
#     extrude(amount=(
#         connector_thickness))

cirque_23mm_pcb.part.color = Color('red')
cirque_23mm_asic.part.color = Color('black')
cirque_23mm_asic.part.position += (0.0, 0.0, cirque_23mm_pcb_plus_adhesive_thickness)
# cirque_23mm_connector.part.color = Color(0.88, 0.87, 0.77)
cirque_23mm_connector.orientation += (90.0, 180.0, 0.0)
cirque_23mm_connector.position += (0.0, 
                                   -connector_y_center_offset, 
                                   (connector_thickness / 2.0) + cirque_23mm_pcb_plus_adhesive_thickness)

cirque_23mm = Compound(label='cirque 23mm', 
                       children=[cirque_23mm_connector,
                                 cirque_23mm_pcb.part, 
                                 cirque_23mm_asic.part,
                                 ])
export_step(cirque_23mm, "./cirque_23mm.step")
show(cirque_23mm)