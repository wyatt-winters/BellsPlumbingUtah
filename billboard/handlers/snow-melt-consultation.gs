/**
 * Utah Boiler Experts — Unified niche service lead handler
 * (Same as handlers/service-lead.gs — deploy this file to update the live Web App.)
 *
 * Handles: boiler repair, replacement, emergency, radiant repair, snow-melt.
 * Deploy at script.google.com → Web app (Anyone) → same /exec URL as before.
 */

// ---- CONFIG ----------------------------------------------------------------

var NOTIFICATION_EMAIL = 'tobboilers@gmail.com';
var SPREADSHEET_ID     = '';
var DEFAULT_REDIRECT   = 'https://utahboilerexperts.com/?submitted=1';
var SITE_ORIGIN        = 'https://utahboilerexperts.com';

// ---- HANDLER ---------------------------------------------------------------

function doPost(e) {
  try {
    var p = (e && e.parameter) ? e.parameter : {};

    if (p.website) {
      return redirect(safeRedirect(p.redirect));
    }

    var name     = trim(p.name);
    var phone    = trim(p.phone);
    var email    = trim(p.email);
    var location = trim(p.location);

    if (!name || !phone || !email || !location) {
      return errorPage('Please fill in all required fields and try again.', p.redirect);
    }

    var source     = trim(p.source) || 'website';
    var stage      = trim(p.stage);
    var area       = trim(p.area) || '(not provided)';
    var notes      = trim(p.notes) || '(none)';
    var submitted  = new Date();
    var leadLabel  = leadLabelFor(source);
    var stageLabel = stageLabelFor(source, stage);

    var subject = leadLabel + ' — ' + name + ' (' + location + ')';
    var body = [
      'New lead — ' + leadLabel,
      '',
      'Name:      ' + name,
      'Phone:     ' + phone,
      'Email:     ' + email,
      'Location:  ' + location,
      'Issue:     ' + stageLabel,
      'Details:   ' + area,
      'Notes:     ' + notes,
      '',
      'Source:    ' + source,
      'Submitted: ' + submitted.toLocaleString('en-US', { timeZone: 'America/Denver' }) + ' MT'
    ].join('\n');

    if (NOTIFICATION_EMAIL && NOTIFICATION_EMAIL.indexOf('@') > 0) {
      MailApp.sendEmail({
        to: NOTIFICATION_EMAIL,
        replyTo: email,
        subject: subject,
        body: body
      });
    }

    if (SPREADSHEET_ID) {
      appendToSheet({
        submitted: submitted,
        leadLabel: leadLabel,
        name: name,
        phone: phone,
        email: email,
        location: location,
        stage: stageLabel,
        area: area,
        notes: notes,
        source: source
      });
    }

    return redirect(safeRedirect(p.redirect));

  } catch (err) {
    return errorPage('Something went wrong. Please call (801) 685-3976 instead.', '');
  }
}

function doGet() {
  return redirect(SITE_ORIGIN);
}

// ---- HELPERS ---------------------------------------------------------------

function trim(val) {
  return (val || '').toString().trim();
}

function leadLabelFor(source) {
  var map = {
    'snow-melt-systems-page': 'Snow-Melt Consultation',
    'lp-snow-melt': 'Snow-Melt Consultation (Ad LP)',
    'boiler-repair-page': 'Boiler Repair Request',
    'boiler-replacement-page': 'Boiler Replacement Quote',
    'emergency-boiler-page': 'Emergency Boiler (No Heat)',
    'lp-emergency-boiler': 'Emergency Boiler (Ad LP)',
    'radiant-repair-page': 'Radiant Heat Repair',
    'lp-radiant-repair': 'Radiant Repair (Ad LP)'
  };
  return map[source] || 'Website Lead';
}

function stageLabelFor(source, val) {
  var snow = {
    'planning': 'Planning / researching',
    'building': 'New construction in progress',
    'retrofit': 'Retrofitting an existing driveway',
    'repair': 'Existing snow-melt system having problems'
  };
  var emergency = {
    'no-heat-now': 'No heat right now',
    'leak': 'Boiler leaking water',
    'error-code': 'Error code on display',
    'other-urgent': 'Other urgent issue'
  };
  var repair = {
    'no-heat': 'No heat / won\'t turn on',
    'leak': 'Leaking water',
    'noise': 'Banging / kettling noise',
    'pressure': 'Pressure problems',
    'other': 'Other boiler issue'
  };
  var replace = {
    'planning': 'Researching replacement options',
    'quote-ready': 'Ready for in-home quote',
    'failed': 'Boiler failed — need replacement ASAP'
  };
  var radiant = {
    'cold-spots': 'Cold spots / uneven heat',
    'zone-dead': 'One zone not working',
    'leak': 'Suspected leak in floor loop',
    'other': 'Other radiant issue'
  };

  var src = (source || '').toString();
  var map = snow;
  if (src.indexOf('emergency') >= 0 || src.indexOf('lp-emergency') >= 0) map = emergency;
  else if (src.indexOf('replacement') >= 0) map = replace;
  else if (src.indexOf('radiant') >= 0) map = radiant;
  else if (src.indexOf('repair') >= 0 && src.indexOf('radiant') < 0) map = repair;

  return map[val] || val || '(not specified)';
}

function safeRedirect(url) {
  var target = trim(url) || DEFAULT_REDIRECT;
  if (target.indexOf(SITE_ORIGIN) !== 0) {
    return DEFAULT_REDIRECT;
  }
  return target;
}

function appendToSheet(row) {
  var sheet = SpreadsheetApp.openById(SPREADSHEET_ID).getActiveSheet();
  if (sheet.getLastRow() === 0) {
    sheet.appendRow([
      'Submitted', 'Lead Type', 'Name', 'Phone', 'Email', 'Location',
      'Issue', 'Details', 'Notes', 'Source'
    ]);
  }
  sheet.appendRow([
    row.submitted,
    row.leadLabel,
    row.name,
    row.phone,
    row.email,
    row.location,
    row.stage,
    row.area,
    row.notes,
    row.source
  ]);
}

function redirect(url) {
  var target = url || DEFAULT_REDIRECT;
  return HtmlService.createHtmlOutput(
    '<!DOCTYPE html><html><head>' +
    '<meta charset="utf-8">' +
    '<meta http-equiv="refresh" content="0;url=' + target + '">' +
    '<script>window.location.replace(' + JSON.stringify(target) + ');</script>' +
    '</head><body><p>Redirecting… <a href="' + target + '">Continue</a></p></body></html>'
  );
}

function errorPage(message, backRedirect) {
  var back = safeRedirect(backRedirect) || SITE_ORIGIN;
  return HtmlService.createHtmlOutput(
    '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Form error</title></head>' +
    '<body style="font-family:sans-serif;max-width:480px;margin:40px auto;padding:0 20px;">' +
    '<h1>Could not submit</h1><p>' + message + '</p>' +
    '<p><a href="' + back + '">← Go back</a></p>' +
    '</body></html>'
  );
}
