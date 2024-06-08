"""Script to generate an ERD diagram using Graphviz."""

from graphviz import Digraph


def generate_erd(output_path: str) -> None:
    """Generate an ERD diagram and save it to the specified path.

    Args:
    ----
        output_path (str): The path where the ERD diagram will be saved.
    """
    # Initialize a directed graph
    dot = Digraph()

    # Define nodes in a more detailed table format without circles around tables, and include datatypes
    dot.node(
        "C",
        """<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
    <TR><TD COLSPAN="2"><B>campaigns</B></TD></TR>
    <TR><TD>campaign_id (PK)</TD><TD>String(50)</TD></TR>
    <TR><TD>campaign_name</TD><TD>String(100)</TD></TR>
    <TR><TD>description</TD><TD>Text</TD></TR>
    <TR><TD>created_at</TD><TD>DateTime</TD></TR></TABLE>>""",
    )

    dot.node(
        "O",
        """<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
    <TR><TD COLSPAN="2"><B>offers</B></TD></TR>
    <TR><TD>offer_id (PK)</TD><TD>String(50)</TD></TR>
    <TR><TD>offer_name</TD><TD>String(100)</TD></TR>
    <TR><TD>offer_link</TD><TD>Text</TD></TR>
    <TR><TD>created_at</TD><TD>DateTime</TD></TR></TABLE>>""",
    )

    dot.node(
        "L",
        """<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
    <TR><TD COLSPAN="2"><B>landers</B></TD></TR>
    <TR><TD>lander_id (PK)</TD><TD>String(50)</TD></TR>
    <TR><TD>lander_name</TD><TD>String(100)</TD></TR>
    <TR><TD>lander_url</TD><TD>Text</TD></TR>
    <TR><TD>created_at</TD><TD>DateTime</TD></TR></TABLE>>""",
    )

    dot.node(
        "CL",
        """<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
    <TR><TD COLSPAN="2"><B>clicks</B></TD></TR>
    <TR><TD>click_id (PK)</TD><TD>String(50)</TD></TR>
    <TR><TD>campaign_id (FK)</TD><TD>String(50)</TD></TR>
    <TR><TD>offer_id (FK)</TD><TD>String(50)</TD></TR>
    <TR><TD>lander_id (FK)</TD><TD>String(50)</TD></TR>
    <TR><TD>timestamp</TD><TD>DateTime</TD></TR></TABLE>>""",
    )

    dot.node(
        "F",
        """<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
    <TR><TD COLSPAN="2"><B>form_data</B></TD></TR>
    <TR><TD>form_submit_id (PK)</TD><TD>String(50)</TD></TR>
    <TR><TD>click_id (FK)</TD><TD>String(50)</TD></TR>
    <TR><TD>first_name</TD><TD>String(50)</TD></TR>
    <TR><TD>last_name</TD><TD>String(50)</TD></TR>
    <TR><TD>telephone</TD><TD>String(50)</TD></TR>
    <TR><TD>city</TD><TD>String(50)</TD></TR>
    <TR><TD>postcode</TD><TD>String(20)</TD></TR>
    <TR><TD>country</TD><TD>String(50)</TD></TR>
    <TR><TD>address</TD><TD>Text</TD></TR>
    <TR><TD>offer_link</TD><TD>Text</TD></TR>
    <TR><TD>user_agent</TD><TD>Text</TD></TR>
    <TR><TD>ip_address</TD><TD>String(50)</TD></TR>
    <TR><TD>timestamp</TD><TD>DateTime</TD></TR></TABLE>>""",
    )

    dot.node(
        "CO",
        """<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
    <TR><TD COLSPAN="2"><B>consent_logs</B></TD></TR>
    <TR><TD>consent_id (PK)</TD><TD>String(50)</TD></TR>
    <TR><TD>click_id (FK)</TD><TD>String(50)</TD></TR>
    <TR><TD>consent_given</TD><TD>Boolean</TD></TR>
    <TR><TD>timestamp</TD><TD>DateTime</TD></TR>
    <TR><TD>ip_address</TD><TD>String(50)</TD></TR>
    <TR><TD>user_agent</TD><TD>Text</TD></TR></TABLE>>""",
    )

    dot.node(
        "TR",
        """<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
    <TR><TD COLSPAN="2"><B>tracker_response</B></TD></TR>
    <TR><TD>click_id (FK)</TD><TD>String(50)</TD></TR>
    <TR><TD>type</TD><TD>String(50)</TD></TR>
    <TR><TD>value</TD><TD>String(100)</TD></TR></TABLE>>""",
    )

    # Define edges and their types using straight lines
    dot.edge("C", "CL", label="1:N", style="solid")
    dot.edge("O", "CL", label="1:N", style="solid")
    dot.edge("L", "CL", label="1:N", style="solid")
    dot.edge("CL", "F", label="1:N", style="solid")
    dot.edge("CL", "CO", label="1:1", style="solid")
    dot.edge("CL", "TR", label="1:N", style="solid")

    # Render the graph
    dot.format = "png"
    dot.attr(splines="line")
    dot.attr("node", shape="plaintext")
    dot.render(output_path)


# Generate the ERD and save to specified path
output_path: str = "/Users/Borat/Documents/code/tracker_v2/erd/ERD_diagram_v1"
generate_erd(output_path)
