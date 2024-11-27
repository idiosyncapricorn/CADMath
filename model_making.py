import math


def generate_geometry(
    outer_radius,
    inner_radius=None,
    thickness=None,
    vent_radius=None,
    num_vents=None,
    flange_radius=None,
    flange_thickness=None,
    center_bore_radius=None,
    bearing_seat_radius=None,
    bearing_seat_width=None,
    bolt_pattern_radius=None,
    bolt_hole_radius=None,
    num_bolts=None,
    segments=100
):
    """
    Generates vertices and faces for a generalized geometric model that can include
    features like circular profiles, vents, hubs, and bolt patterns.
    
    :param outer_radius: Outer radius of the main circular feature.
    :param inner_radius: Inner radius (optional for hollow shapes).
    :param thickness: Thickness of the main circular feature.
    :param vent_radius: Radius of vent holes (optional).
    :param num_vents: Number of vent holes (optional).
    :param flange_radius: Outer radius of a flange (optional).
    :param flange_thickness: Thickness of the flange (optional).
    :param center_bore_radius: Radius of a central bore (optional).
    :param bearing_seat_radius: Radius of a cylindrical bearing seat (optional).
    :param bearing_seat_width: Width of the bearing seat (optional).
    :param bolt_pattern_radius: Radius for bolt patterns (optional).
    :param bolt_hole_radius: Radius of bolt holes (optional).
    :param num_bolts: Number of bolts in the pattern (optional).
    :param segments: Number of segments to approximate circular geometry.
    :return: Tuple of (vertices, faces).
    """
    vertices = []
    faces = []

    # Main circular geometry
    if thickness is not None:
        for segment in range(segments):
            theta = 2 * math.pi * segment / segments
            x_outer = outer_radius * math.cos(theta)
            y_outer = outer_radius * math.sin(theta)
            if inner_radius:
                x_inner = inner_radius * math.cos(theta)
                y_inner = inner_radius * math.sin(theta)
            
            vertices.append((x_outer, y_outer, thickness / 2))
            vertices.append((x_outer, y_outer, -thickness / 2))
            if inner_radius:
                vertices.append((x_inner, y_inner, thickness / 2))
                vertices.append((x_inner, y_inner, -thickness / 2))

        for segment in range(segments):
            next_segment = (segment + 1) % segments
            # Outer surface
            faces.append([segment * 4, next_segment * 4, next_segment * 4 + 1])
            faces.append([segment * 4, next_segment * 4 + 1, segment * 4 + 1])
            # Inner surface (if applicable)
            if inner_radius:
                faces.append([segment * 4 + 2, next_segment * 4 + 2, next_segment * 4 + 3])
                faces.append([segment * 4 + 2, next_segment * 4 + 3, segment * 4 + 3])
            # Top face
            if inner_radius:
                faces.append([segment * 4, segment * 4 + 2, next_segment * 4 + 2])
                faces.append([segment * 4, next_segment * 4 + 2, next_segment * 4])
            # Bottom face
                faces.append([segment * 4 + 1, next_segment * 4 + 1, next_segment * 4 + 3])
                faces.append([segment * 4 + 1, next_segment * 4 + 3, segment * 4 + 3])
    

    # Flange geometry
    if flange_radius and flange_thickness:
        start_index = len(vertices)
        for segment in range(segments):
            theta = 2 * math.pi * segment / segments
            x_outer = flange_radius * math.cos(theta)
            y_outer = flange_radius * math.sin(theta)
            x_inner = center_bore_radius * math.cos(theta) if center_bore_radius else 0
            y_inner = center_bore_radius * math.sin(theta) if center_bore_radius else 0

            vertices.append((x_outer, y_outer, flange_thickness / 2))
            vertices.append((x_outer, y_outer, -flange_thickness / 2))
            vertices.append((x_inner, y_inner, flange_thickness / 2))
            vertices.append((x_inner, y_inner, -flange_thickness / 2))

        for segment in range(segments):
            next_segment = (segment + 1) % segments
            faces.append([start_index + segment * 4, start_index + next_segment * 4, start_index + next_segment * 4 + 1])
            faces.append([start_index + segment * 4, start_index + next_segment * 4 + 1, start_index + segment * 4 + 1])

    

    return vertices, faces
