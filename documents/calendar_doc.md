# Google Calendar API Documentation for Python (as of April 21, 2025)

This document provides a summary of the Google Calendar API documentation relevant for Python developers, based on the official Google Developers website.

## 1. Python Quickstart

*(Source: https://developers.google.com/workspace/calendar/api/quickstart/python)*

This quickstart shows you how to run a simple Python command-line application that makes requests to the Google Calendar API.

**Objective:** List the next 10 upcoming events from the user's primary calendar.

**Prerequisites:**

* Python 3.10+
* Pip package manager
* A Google Account with Google Calendar enabled.
* Access to the internet and a web browser.

**Step 1: Turn on the Google Calendar API**

1.  Use the [Google Cloud console wizard](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com) to create or select a project and automatically turn on the API. Click **Continue**, then **Go to credentials**.
2.  On the **Add credentials to your project** page, click **+ Create Credentials** > **OAuth client ID**.
3.  Select **Desktop app** for the Application type.
4.  In the **Name** field, type a name for the credential (e.g., "Calendar API Desktop Quickstart").
5.  Click **Create**. The OAuth client created screen appears, showing your Client ID and Client secret.
6.  Click **Download JSON**. Save the file as `credentials.json` in your working directory.

**Step 2: Install the Google Client Library**

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


Step 3: Set up the sample
Create a file named quickstart.py in your working directory and copy the following code:
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["[https://www.googleapis.com/auth/calendar.readonly](https://www.googleapis.com/auth/calendar.readonly)"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()


Step 4: Run the sample
Run the script from your terminal:
python quickstart.py


The first time you run it, you'll be prompted to authorize access:
If you aren't logged into your Google Account, you'll be prompted to log in.
If you're logged into multiple accounts, select one for authorization.
Click Accept.
The script completes, and prints the upcoming events from your primary calendar.
Subsequent runs will use the stored credentials in token.json (in the same directory).
Troubleshooting:
AttributeError: module 'collections' has no attribute 'MutableMapping': This can happen if google-auth was installed with an older pip version. Upgrade pip (pip install -U pip) and reinstall the libraries.
TypeError: sequence item 0: expected str instance, bytes found: Often due to incompatibility with httplib2. Uninstall it (pip uninstall httplib2) and reinstall (pip install httplib2).
Authorization errors: Ensure credentials.json was downloaded correctly and is in the right directory. Delete token.json and re-run to re-authorize if needed.
2. API Concepts Overview
(Source: https://developers.google.com/workspace/calendar/api/concepts)
The Google Calendar API lets you integrate your app with Google Calendar, providing programmatic access to calendar data and functionality.
Key Concepts:
Calendars: A collection of events. Each user has at least one primary calendar. Additional secondary calendars can be created, shared, or subscribed to.
Events: Objects associated with a specific date or time range, containing details like summary, description, location, attendees, reminders, etc. Events can be single occurrences or recurring.
Settings: User-specific preferences like time zone, default reminders, etc.
Access Control Lists (ACLs): Control how calendars are shared with other users or groups.
Resources: The API is structured around resources like Calendars, Events, Settings, Acl, etc. Each resource type has associated methods (e.g., events.list, events.insert).
Authorization: Uses OAuth 2.0 for authentication and authorization. Different scopes grant different levels of access (e.g., read-only vs. read-write).
Push Notifications: Allows your application to be notified in real-time when calendar data changes, avoiding the need for constant polling. (See Section 10)
Sync Tokens: Enables efficient synchronization by fetching only the changes since the last sync. (See Section 11)
Time Zones: Crucial for correctly interpreting event start/end times. (See Section 12)
Recurring Events: Events that repeat based on defined rules. (See Section 13)
3. Resource Types
(Source: https://developers.google.com/workspace/calendar/api/resource_types)
The API defines several primary resource types:
CalendarList: A collection of all calendar entries the user has access to (primary, secondary, subscribed). Use calendarList.list to retrieve it.
CalendarListEntry: Represents a single calendar in the user's list (e.g., "Work Calendar", "Personal Calendar"). Contains ID, summary, color, access role, etc.
Calendars: Represents a single calendar's metadata (e.g., title, description, time zone). Use calendars.get to retrieve details for a specific calendarId.
Events: Represents an event within a calendar. Contains details like start/end times, summary, attendees, location, status, recurrence rules, reminders, etc. Use events.list, events.get, events.insert, events.update, events.delete, events.instances.
Settings: User-specific settings affecting their Calendar experience. Use settings.list, settings.get.
Setting: Represents a single key-value pair for a setting (e.g., weekStart, format).
Acl: Represents the Access Control List for a calendar, defining sharing rules. Use acl.list, acl.get, acl.insert, acl.update, acl.delete.
AclRule: Represents a single rule granting access to a specific user, group, or domain with a particular role (e.g., reader, writer, owner).
Colors: Defines the standard color palettes available for calendars and events. Use colors.get.
Freebusy: Allows querying for free/busy time slots across a set of calendars. Use freebusy.query.
Each resource has a specific JSON representation and associated API methods. Refer to the API Reference for detailed structures and methods.
4. Events and Calendars
(Source: https://developers.google.com/workspace/calendar/api/concepts/events-calendars)
Calendars:
Primary Calendar: Every user has one, tied to their Google Account. Cannot be deleted or un-shared by the primary owner. Identified by the calendarId "primary".
Secondary Calendars: Created by users. Can be modified, deleted, and shared. Have unique calendarIds (often look like email addresses).
CalendarList: The user's list of all calendars they have access to (primary, owned secondary, shared secondary). Use calendarList.list to see them.
Creating Calendars: Use calendars.insert.
Modifying Metadata: Use calendars.update or calendars.patch.
Deleting Calendars: Use calendars.delete (only for secondary calendars you own).
Clearing Calendars: Use calendars.clear to delete all events from a primary calendar (cannot delete the calendar itself).
Events:
Representation: Defined by the Events resource. Key fields include summary, start, end, attendees, location, description, recurrence, reminders.
Time Zones: See Section 12.
Creating Events: Use events.insert. Specify the calendarId.
Retrieving Events: Use events.list (multiple events) or events.get (single event by eventId).
Updating Events: Use events.update or events.patch. Requires the eventId. Use ETags for conditional updates (See Section 9.1). Use fields for partial updates (See Section 9.2).
Deleting Events: Use events.delete. Requires the eventId.
Recurring Events: See Section 13.
Importing Events: Use events.import to copy events between calendars, potentially changing organizer or UID.
5. Sharing and ACLs
(Source: https://developers.google.com/workspace/calendar/api/concepts/sharing)
Sharing is managed via Access Control Lists (ACLs). Each calendar has an ACL that specifies who can access the calendar and what level of permission they have.
ACL Rules (AclRule resource):
Scope: Defines who the rule applies to.
type: user, group, domain, default (public access).
value: Email address, group address, domain name (or empty for default).
Role: Defines the permission level.
none: No access. Effectively removes access.
freeBusyReader: Can see free/busy information only.
reader: Can see event details (read-only).
writer: Can read and modify events.
owner: Full control, including sharing settings and deletion (for secondary calendars).
Managing ACLs:
Listing Rules: Use acl.list for a given calendarId.
Adding/Updating Rules: Use acl.insert or acl.update. Specify the ruleId (usually scope_type:scope_value), scope, and role.
Removing Rules: Use acl.delete.
Example: Share a calendar with a user for read access:
# Assume 'service' is an authenticated build object
# Assume 'calendar_id' is the ID of the calendar to share

rule = {
  'scope': {
    'type': 'user',
    'value': 'user@example.com', # Email of the user to share with
  },
  'role': 'reader'
}

created_rule = service.acl().insert(calendarId=calendar_id, body=rule).execute()
print(f"Rule created for {created_rule['id']}")


6. Inviting Attendees to Events
(Source: https://developers.google.com/workspace/calendar/api/concepts/inviting-attendees-to-events)
You can manage event attendees directly through the API.
Key Concepts:
Attendees Field: The attendees property in the Events resource is a list of objects, each representing an attendee.
Attendee Properties:
email: The attendee's email address (required).
displayName: Optional name.
organizer: Boolean, true if this attendee is the event organizer.
self: Boolean, true if this attendee represents the user making the API request.
resource: Boolean, true if this attendee is a resource (e.g., meeting room).
optional: Boolean, true if attendance is optional.
responseStatus: The attendee's status (needsAction, declined, tentative, accepted).
comment: Optional comment provided by the attendee.
Adding Attendees: Include their details in the attendees list when calling events.insert or events.update.
Modifying Attendees: Fetch the event using events.get, modify the attendees list, and use events.update.
Removing Attendees: Fetch the event, remove the attendee object from the attendees list, and use events.update.
Sending Notifications: Use the sendNotifications or sendUpdates parameter in insert/update/delete methods to control whether email notifications are sent to attendees.
sendNotifications=true: Send invitations/updates to newly added/modified attendees.
sendUpdates='all': Notify all attendees of changes.
sendUpdates='externalOnly': Notify only attendees outside the organizer's domain.
sendUpdates='none': Do not send notifications.
Example: Adding an attendee during event creation:
# Assume 'service' is an authenticated build object
# Assume 'calendar_id' is the ID of the target calendar

event = {
  'summary': 'Team Meeting',
  'location': 'Conference Room B',
  'description': 'Discuss project milestones.',
  'start': {
    'dateTime': '2025-05-15T09:00:00-07:00', # Example time
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2025-05-15T10:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'attendees': [
    {'email': 'attendee1@example.com'},
    {'email': 'attendee2@example.com', 'optional': True},
  ],
  # Other event properties...
}

# Set sendUpdates=all to notify attendees
created_event = service.events().insert(calendarId=calendar_id, body=event, sendUpdates='all').execute()
print(f"Event created: {created_event.get('htmlLink')}")


7. Reminders and Notifications
(Source: https://developers.google.com/workspace/calendar/api/concepts/reminders)
Reminders help users remember upcoming events. They can be configured per-event or as defaults for a calendar.
Reminder Types:
email: Sends an email reminder.
popup: Shows a pop-up notification in Google Calendar web/mobile interfaces.
Configuring Reminders:
Event-Specific Reminders: Set the reminders property within the Events resource.
useDefault: Boolean. If true, use the calendar's default reminders. If false (or omitted), use the overrides.
overrides: A list of reminder objects specifying the notification method and time.
method: email or popup.
minutes: Number of minutes before the event start time to trigger the reminder.
Default Calendar Reminders: Users configure these in their Google Calendar settings. The Events resource reminders.useDefault flag respects these user-defined defaults. The API doesn't allow modifying another user's default reminders.
Example: Setting a pop-up reminder 10 minutes before and an email reminder 1 hour before an event:
event = {
  # ... other event properties ...
  'reminders': {
    'useDefault': False, # Override the default reminders
    'overrides': [
      {'method': 'popup', 'minutes': 10},
      {'method': 'email', 'minutes': 60}
    ]
  }
}

# Use this event body with events.insert or events.update


Push Notifications (Server-to-Server):
See Section 10 for details on setting up real-time notifications to your server.
8. Domain-Wide Delegation (Google Workspace)
(Source: https://developers.google.com/workspace/calendar/api/concepts/domain)
For Google Workspace domains, administrators can grant applications domain-wide authority to access user data without requiring individual user consent. This is useful for applications that need to manage calendars across the organization.
Key Steps:
Create a Service Account: In the Google Cloud Console, create a service account for your application. Download its private key file.
Delegate Domain-Wide Authority:
Go to your Google Workspace domain's Admin console (admin.google.com).
Navigate to Security > Access and data control > API controls.
In the "Domain wide delegation" section, click "Manage Domain Wide Delegation".
Click "Add new".
Enter the service account's Client ID.
Enter the required OAuth scopes (e.g., https://www.googleapis.com/auth/calendar, https://www.googleapis.com/auth/calendar.events).
Click "Authorize".
Impersonate Users in Code: Use the service account credentials and specify the email address of the user to impersonate when building the service object.
Example (using google-auth library):
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SERVICE_ACCOUNT_FILE = 'path/to/your/service_account_key.json'
SCOPES = ['[https://www.googleapis.com/auth/calendar](https://www.googleapis.com/auth/calendar)'] # Or other needed scopes
USER_TO_IMPERSONATE = 'user@yourdomain.com' # The target user's email

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Delegate access to the target user
delegated_creds = creds.with_subject(USER_TO_IMPERSONATE)

try:
    service = build('calendar', 'v3', credentials=delegated_creds)

    # Now you can make API calls as if you were USER_TO_IMPERSONATE
    calendar_list = service.calendarList().list().execute()
    print(f"Accessing calendars for {USER_TO_IMPERSONATE}:")
    for item in calendar_list.get('items', []):
        print(f"- {item.get('summary')} ({item.get('id')})")

except HttpError as error:
    print(f"An error occurred: {error}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


Important Considerations:
Domain-wide delegation grants significant access. Use it carefully and only grant necessary scopes.
Only Google Workspace administrators can configure domain-wide delegation.
9. Performance Best Practices
(Source: https://developers.google.com/calendar/api/guides/performance)
Improve your application's performance and avoid hitting rate limits by using these techniques:
9.1 ETags for Conditional Retrieval
What it is: ETags are identifiers for specific versions of a resource. When you retrieve a resource, the response includes an ETag HTTP header.
How to use: Store the ETag along with the resource data. When requesting the resource again, include the ETag in the If-None-Match HTTP request header.
Benefit: If the resource hasn't changed, the server responds with 304 Not Modified and an empty body, saving bandwidth and processing time. If it has changed, the server returns the full, updated resource with the new ETag.
Python Client Library: The library typically handles ETags automatically for get operations when caching is enabled, but you might need manual handling for update/patch (using the ETag in If-Match for conditional updates to prevent lost updates).
9.2 Partial Response (Fields Parameter)
What it is: Request only the specific fields of a resource you actually need.
How to use: Add the fields query parameter to your API request, specifying the desired fields using a comma-separated list and nested syntax (e.g., fields=items(id,summary,start,end),nextPageToken).
Benefit: Reduces bandwidth usage and latency by avoiding the transfer and parsing of unnecessary data.
Example (Python Client Library): Many list or get methods accept a fields argument.
# Get only event id and summary
events = service.events().list(
    calendarId='primary',
    fields='items(id,summary)'
).execute()


9.3 Partial Update (Patch)
What it is: Modify only the fields that have changed in a resource, instead of sending the entire resource representation.
How to use: Use the HTTP PATCH method (supported by update methods in the client library when used correctly, often implicitly). Provide only the fields you want to change in the request body. For resources with ETags, include the ETag in an If-Match header to ensure you're updating the correct version.
Benefit: Saves bandwidth and avoids potential conflicts if multiple clients are updating the same resource.
Python Client Library: The service.resource().patch() method is designed for this. You provide the resourceId, and a body containing only the fields to update.
# Assume 'event_id' and 'etag' are known
updated_fields = {
    'summary': 'Updated Event Summary'
}
# Note: ETag handling might be needed via headers or specific library features
updated_event = service.events().patch(
    calendarId='primary',
    eventId=event_id,
    body=updated_fields
    # Potentially add headers={'If-Match': etag} if library doesn't handle automatically
).execute()

(Note: Check library specifics for ETag handling with patch)
9.4 Batch Requests
What it is: Combine multiple independent API calls into a single HTTP request.
How to use: Create a batch request containing multiple API calls (e.g., inserting several events, deleting a few ACL rules). Send this single multipart request to the API's batch endpoint (https://www.googleapis.com/batch/calendar/v3).
Benefit: Reduces the number of HTTP connections your client needs to make, significantly improving efficiency, especially for numerous small operations. Each inner request still counts towards your quota.
Python Client Library: Provides utilities for creating and executing batch requests.
from googleapiclient.http import BatchHttpRequest

def list_events_callback(request_id, response, exception):
  if exception:
    print(f"Error for {request_id}: {exception}")
  else:
    print(f"Events for {request_id}: {len(response.get('items', []))}")

batch = service.new_batch_http_request(callback=list_events_callback)

batch.add(service.events().list(calendarId='primary', q='Meeting A'), request_id='req1')
batch.add(service.events().list(calendarId='primary', q='Meeting B'), request_id='req2')
# Add more requests...

batch.execute()


9.5 Use Gzip Compression
What it is: Compress API responses to reduce bandwidth.
How to use:
Add Accept-Encoding: gzip to your request headers.
Add User-Agent containing the string gzip.
Benefit: Significantly reduces the size of API responses, saving bandwidth.
Python Client Library: The google-api-python-client handles Gzip compression automatically when available.
10. Push Notifications
(Source: https://developers.google.com/calendar/api/guides/push)
Receive notifications at your server endpoint when watched resources change, instead of polling.
Steps:
Register Your Domain: Verify ownership of your receiving domain/URL in the Google Cloud Console project.
Set up HTTPS Server: Your server must handle HTTPS POST requests at the notification endpoint URL.
Watch Resources: Call the watch() method for the desired resource (e.g., events.watch, acl.watch, settings.watch, calendarList.watch).
Provide a request body specifying:
id: A unique identifier for the notification channel.
type: Must be web_hook.
address: The HTTPS URL where notifications should be sent.
Optional: token (secret verification token), params.
Handle Notifications:
Your server will receive a sync message when the channel is first created.
Subsequently, it will receive POST requests when watched resources change.
Respond Quickly: Acknowledge notifications promptly with a success status code (e.g., 200 OK). Process the actual changes asynchronously.
Check Headers: Verify the notification using headers like X-Goog-Channel-ID, X-Goog-Resource-ID, X-Goog-Resource-State (exists, not_exists, sync), X-Goog-Channel-Token (if you provided one).
Fetch Changes: If the state is exists, use the resource ID and potentially a sync token (see Section 11) to fetch the actual changes.
Stop Notifications: Call the stop() method for the channel using Channels.stop with the channel id and resourceId from the original watch response. Channels expire automatically after a certain duration.
Example: Watching events on the primary calendar:
import uuid

channel_id = str(uuid.uuid4()) # Generate a unique ID
watch_request_body = {
  'id': channel_id,
  'type': 'web_hook',
  'address': '[https://yourdomain.com/notifications](https://yourdomain.com/notifications)' # Your HTTPS endpoint
  # 'token': 'your-secret-token' # Optional verification token
}

# Ensure you have write scope (e.g., [https://www.googleapis.com/auth/calendar](https://www.googleapis.com/auth/calendar))
# The response contains channel details including resourceId and expiration
watch_response = service.events().watch(calendarId='primary', body=watch_request_body).execute()
print(f"Watch channel created: {watch_response}")

# Later, to stop:
# stop_channel_body = {
#   'id': watch_response['id'],
#   'resourceId': watch_response['resourceId']
# }
# service.channels().stop(body=stop_channel_body).execute()


11. Sync Tokens
(Source: https://developers.google.com/calendar/api/guides/sync)
Efficiently synchronize calendar data by retrieving only the changes since the last sync.
Process:
Initial Full Sync: Perform an initial events.list (or calendarList.list, etc.) request without a sync token.
The response will contain the first page of results and a nextSyncToken field on the last page.
Store this nextSyncToken securely.
Incremental Sync: For subsequent syncs, call events.list again, but this time provide the stored token in the syncToken parameter.
The response will contain only the resources that have changed (created, updated, deleted) since that token was generated.
Deleted items will have their status set to cancelled.
The response will include a new nextSyncToken. Store this new token, replacing the old one.
Handling Token Expiration: Sync tokens expire (e.g., after ~7 days of inactivity or other reasons). If a request with a syncToken returns an HTTP 410 Gone error, the token is invalid. Discard it and perform a full sync (Step 1) again to get a new baseline and a new nextSyncToken.
Benefits:
Massively reduces bandwidth and processing compared to fetching all data every time.
Essential for applications needing up-to-date calendar information.
Example:
sync_token = load_stored_sync_token() # Load from your storage

try:
    if sync_token:
        print("Performing incremental sync...")
        events_result = service.events().list(
            calendarId='primary',
            syncToken=sync_token
        ).execute()
    else:
        print("Performing full sync...")
        events_result = service.events().list(calendarId='primary').execute()
        # Need to paginate through all results using nextPageToken
        # to get the nextSyncToken from the *last* page.
        # (Simplified here - real implementation needs pagination loop)

    items = events_result.get('items', [])
    # Process changed items...
    for event in items:
        if event.get('status') == 'cancelled':
            print(f"Event deleted: {event['id']}")
        else:
            print(f"Event changed: {event['id']} - {event.get('summary')}")

    next_sync_token = events_result.get('nextSyncToken')
    if next_sync_token:
        save_sync_token(next_sync_token) # Save for next time

except HttpError as error:
    if error.resp.status == 410:
        print("Sync token expired. Performing full sync.")
        clear_stored_sync_token()
        # Re-run the full sync logic (Step 1)
    else:
        print(f"An error occurred: {error}")



(Note: Full sync requires handling pagination with nextPageToken to find the nextSyncToken on the final page.)
12. Time Zones
(Source: https://developers.google.com/calendar/api/concepts/events-calendars#time_zones)
Google Calendar stores all events in UTC but displays them in the user's local time zone. Specifying time zones correctly is crucial.
Key Points:
Calendar Time Zone: Each calendar has a default time zone setting (timeZone field in the Calendars resource).
Event Time Specification:
Specific Time Zone: Use dateTime fields for start/end times, including a valid IANA time zone identifier (e.g., America/Los_Angeles, Europe/Zurich) in the timeZone sub-field. The dateTime value itself should represent the local time in that zone (e.g., 2025-05-20T10:00:00).
Floating Time (Rare): Omit the timeZone sub-field. The event occurs at the specified clock time in whatever time zone the viewer is currently in. Use with caution.
UTC Offset: Use dateTime fields with a UTC offset (e.g., 2025-05-20T17:00:00Z or 2025-05-20T10:00:00-07:00). The API will typically convert this to the calendar's time zone.
All-Day Events: Use date fields (e.g., 2025-05-20) instead of dateTime. These events span the entire day, independent of time zone.
API Behavior:
When creating/updating events with dateTime and timeZone, the API stores the UTC equivalent.
When retrieving events, the API usually returns dateTime in the event's specified timeZone or the calendar's timeZone if none was set on the event. All-day events return date.
Best Practice: Always specify the timeZone for events with specific start/end times using IANA identifiers. Relying on UTC offsets can be problematic with Daylight Saving Time transitions.
Example: Creating an event in a specific time zone:
event = {
  'summary': 'Event in New York',
  'start': {
    'dateTime': '2025-06-01T14:00:00', # 2 PM
    'timeZone': 'America/New_York'
  },
  'end': {
    'dateTime': '2025-06-01T15:30:00', # 3:30 PM
    'timeZone': 'America/New_York'
  },
  # ... other properties
}

created_event = service.events().insert(calendarId='primary', body=event).execute()


13. Recurring Events
(Source: https://developers.google.com/calendar/api/concepts/recurringevents)
Events can be set to repeat based on rules defined in the iCalendar specification (RFC 5545).
Key Concepts:
Recurrence Rules: Specified in the recurrence field of the Events resource. This is a list of strings representing RRULE, RDATE, EXRULE, and EXDATE properties.
RRULE: Defines the main repetition pattern (e.g., FREQ=WEEKLY;BYDAY=MO;UNTIL=20251231T...).
RDATE: Specifies additional dates/times when the event occurs.
EXRULE: Defines exceptions to the RRULE pattern.
EXDATE: Specifies specific dates/times when the event does not occur, even if it falls within the RRULE.
Master Event: The API treats a recurring event as a single "master" event containing the recurrence rules. It has a unique eventId.
Instances: Individual occurrences of a recurring event. They generally share the same eventId as the master but have a unique recurringEventId field pointing back to the master.
Exceptions: If an instance is modified (e.g., time changed, summary updated, attendee added/removed), it becomes an "exception". It gets its own unique eventId (different from the master) but retains the recurringEventId. Its status might change (e.g., confirmed). The original instance time slot in the master recurrence is effectively cancelled (status: cancelled).
Retrieving Instances: Use events.list with singleEvents=True. This expands recurring events into their individual instances within the specified time range (timeMin, timeMax). This is the most common way to display events to users.
Retrieving Master/Exceptions: Use events.list with singleEvents=False (default). This returns only master events and exceptions.
Retrieving Specific Instances: Use events.instances with the eventId of the master recurring event.
Updating/Deleting:
Modifying the master event (events.update/patch on the master eventId) affects all future instances (unless they are exceptions).
Deleting the master event (events.delete on the master eventId) deletes all instances.
Modifying a single instance (using events.update/patch on its specific instance eventId obtained via singleEvents=True or events.instances) creates an exception.
Deleting a single instance (events.delete on its instance eventId) cancels that specific occurrence and potentially creates an exception marker.
Example: Creating a weekly recurring event:
event = {
  'summary': 'Weekly Status Meeting',
  'location': 'Virtual',
  'start': {
    'dateTime': '2025-05-05T10:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2025-05-05T10:30:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=WEEKLY;BYDAY=MO;UNTIL=20251231T103000Z' # Every Monday until end of 2025 (UTC time for UNTIL)
  ],
  # ... attendees, reminders etc.
}

created_event = service.events().insert(calendarId='primary', body=event).execute()
print(f"Recurring event created: {created_event.get('id')}")


14. Handling API Errors
(Source: https://developers.google.com/calendar/api/guides/errors)
API requests can fail. Your application should handle potential errors gracefully.
Error Response Format:
Errors are returned as JSON objects, typically including:
{
  "error": {
    "errors": [
      {
        "domain": "global", // or "calendar"
        "reason": "invalid", // e.g., required, forbidden, notFound, invalidParameter
        "message": "Invalid Value" // Human-readable description
        // "locationType": "parameter", // Where the error occurred
        // "location": "calendarId" // Specific parameter/field
      }
    ],
    "code": 400, // HTTP status code
    "message": "Invalid Value"
  }
}


Common HTTP Status Codes:
400 Bad Request: Invalid syntax, missing required field (e.g., invalid, required).
401 Unauthorized: Invalid or missing credentials. Refresh OAuth token if possible.
403 Forbidden: Insufficient permissions, rate limit exceeded, calendar usage limits exceeded (e.g., forbidden, rateLimitExceeded, calendarUsageLimitsExceeded, dailyLimitExceeded). Implement exponential backoff.
404 Not Found: Resource doesn't exist (e.g., notFound).
409 Conflict: Resource already exists (e.g., when creating with an ID that's taken) or optimistic concurrency control failure (ETag mismatch).
410 Gone: Resource no longer available (often seen with expired sync tokens or deleted push channels). Perform a full sync or re-establish the channel.
412 Precondition Failed: ETag mismatch (e.g., conditionNotMet). Fetch the latest version and retry.
500 Internal Server Error, 503 Service Unavailable: Temporary server-side issue. Use exponential backoff and retry.
Error Handling Strategy:
Catch Exceptions: Use try...except HttpError blocks around API calls.
Inspect Error: Examine the HttpError object (error.resp.status, error.content) to understand the cause.
Implement Retries with Exponential Backoff: For transient errors (5xx, 403 rate limits), wait progressively longer intervals before retrying (e.g., 1s, 2s, 4s, 8s + random jitter). Stop after a maximum number of retries or time.
Handle Specific Errors:
401: Attempt token refresh; if fails, prompt user re-authentication.
410 (Sync Token): Perform full sync.
404: Inform user resource not found.
403 (Permissions): Inform user they lack permissions.
400, 422: Log the error; likely a bug in your request construction.
Log Errors: Record detailed error information for debugging.
Exponential Backoff Example (Conceptual):
import time
import random
from googleapiclient.errors import HttpError

retries = 0
max_retries = 5
base_backoff = 1 # seconds

while retries < max_retries:
    try:
        # Make API call, e.g., service.events().list(...).execute()
        result = make_api_call()
        # Success! Process result and break loop
        process(result)
        break
    except HttpError as error:
        if error.resp.status in [403, 500, 503]: # Retryable errors
            retries += 1
            if retries >= max_retries:
                print(f"Max retries reached. Error: {error}")
                # Handle final failure
                break
            wait_time = (base_backoff * (2 ** (retries - 1))) + random.uniform(0, 1)
            print(f"Retryable error ({error.resp.status}). Retrying in {wait_time:.2f} seconds...")
            time.sleep(wait_time)
        else:
            # Non-retryable error (400, 401, 404, etc.)
            print(f"Non-retryable error: {error}")
            # Handle specific error or raise it
            raise error # or handle appropriately
    except Exception as e:
        # Other unexpected errors
        print(f"An unexpected error occurred: {e}")
        raise e


15. Usage Limits (Quotas)
(Source: Based on general Google API & Workspace documentation principles, specific limits may vary)
The Google Calendar API enforces usage limits to ensure service availability and prevent abuse.
Types of Limits:
Rate Limits: Limit the number of requests per unit of time (e.g., queries per second per user, queries per 100 seconds per project). Often enforced with 403 rateLimitExceeded errors.
Daily Quota: A total number of requests allowed per day for your project. Resets daily (usually Pacific Time midnight). Exceeding this results in 403 dailyLimitExceeded.
Calendar Usage Limits: Limits on the number of calendars or events a user can create or be subscribed to. May result in 403 calendarUsageLimitsExceeded.
Viewing Your Quotas:
Go to the Google Cloud Console.
Navigate to your project.
Go to "APIs & Services" > "Enabled APIs & services".
Select "Google Calendar API".
Click the "Quotas" tab.
Best Practices:
Implement exponential backoff for rate limit errors (403).
Use performance best practices (ETags, partial response, batching, sync tokens, push notifications) to reduce the number of requests.
Monitor your usage in the Cloud Console.
Request higher quotas via the Cloud Console if your legitimate application needs exceed the defaults (requires justification).
Further Reading:
Google Calendar API Reference
Google API Client Library for Python
[Authorization Scopes for Google APIs]
