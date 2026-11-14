#!/usr/bin/python3
"""Generate individual invitations by substituting template placeholders."""


def generate_invitations(template, attendees):
    """Write an invitation for each attendee to a numbered text file."""
    if not isinstance(template, str):
        print("Invalid input type: template must be a string.")
        return
    if not isinstance(attendees, list) or not all(
            isinstance(attendee, dict) for attendee in attendees):
        print("Invalid input type: attendees must be a list of dictionaries.")
        return
    if not template.strip():
        print("Template is empty, no output files generated.")
        return
    if not attendees:
        print("No data provided, no output files generated.")
        return

    fields = ("name", "event_title", "event_date", "event_location")
    for index, attendee in enumerate(attendees, start=1):
        invitation = template
        for field in fields:
            value = attendee.get(field)
            if value is None or value == "":
                value = "N/A"
            invitation = invitation.replace("{" + field + "}", str(value))

        filename = "output_{}.txt".format(index)
        try:
            with open(filename, "w", encoding="utf-8") as output:
                output.write(invitation)
        except OSError as error:
            print("Error writing {}: {}".format(filename, error))
