-- Run individual SELECTs through: opencode db "<SQL>" --format json
-- Read-only projections; do not select raw metadata, credentials or encrypted reasoning.
-- DB: /home/denis/.local/share/opencode/opencode.db (CLI supported interface).

SELECT id,parent_id,title,time_created,time_updated FROM session WHERE id IN ('ses_f0e3bd4e4ffem8jmapJbWHWjLz','ses_ef4efdc0bffeP1H6Ul9qC57zdH','ses_eeeb9dea3ffeqyVQdiPzOLUHGF');

SELECT id,time_created,time_updated,json_extract(data,'$.state.status') status,json_extract(data,'$.state.input.description') description,json_extract(data,'$.state.metadata.sessionId') child,json_extract(data,'$.state.time') time FROM part WHERE session_id='ses_f0e3bd4e4ffem8jmapJbWHWjLz' AND json_extract(data,'$.tool')='task' AND json_extract(data,'$.state.metadata.sessionId') IN ('ses_ef4efdc0bffeP1H6Ul9qC57zdH','ses_eeeb9dea3ffeqyVQdiPzOLUHGF') ORDER BY time_created;

SELECT id,time_created,time_updated,json_extract(data,'$.role') role,json_extract(data,'$.time') time,json_extract(data,'$.modelID') model,json_extract(data,'$.finish') finish,json_extract(data,'$.error') error,json_extract(data,'$.tokens') tokens FROM message WHERE session_id='ses_ef4efdc0bffeP1H6Ul9qC57zdH' AND time_created>=1791203770000 ORDER BY time_created;

SELECT id,time_created,time_updated,json_extract(data,'$.type') type,json_extract(data,'$.time') part_time FROM part WHERE message_id='msg_10c222f68001MgHl1Jf8gBzsnO' ORDER BY time_created;

SELECT json_extract(data,'$.type') type,count(*) n,min(time_created) first,max(time_updated) last,min(json_extract(data,'$.time.start')) start,max(json_extract(data,'$.time.end')) end FROM part WHERE message_id='msg_10c222f68001MgHl1Jf8gBzsnO' GROUP BY type;

SELECT id,time_created,json_extract(data,'$.type') type,json_extract(data,'$.tool') tool,json_extract(data,'$.state.status') status,json_extract(data,'$.state.time') tool_time,substr(json_extract(data,'$.text'),1,2200) text,substr(json_extract(data,'$.state.input.command'),1,1600) command,substr(json_extract(data,'$.state.output'),1,2200) output FROM part WHERE session_id='ses_ef4efdc0bffeP1H6Ul9qC57zdH' AND json_extract(data,'$.type')!='reasoning' ORDER BY time_created DESC LIMIT 18;

SELECT json_extract(data,'$.state.status') status,count(*) n FROM part WHERE session_id='ses_ef4efdc0bffeP1H6Ul9qC57zdH' AND json_extract(data,'$.type')='tool' GROUP BY status;

SELECT count(*) n FROM part WHERE session_id='ses_ef4efdc0bffeP1H6Ul9qC57zdH' AND json_extract(data,'$.type')='tool' AND time_created>=1791291049327;

SELECT id,seq,type,json_extract(data,'$.part.id') part_id,json_extract(data,'$.part.type') part_type,json_extract(data,'$.part.time') part_time,json_extract(data,'$.info.id') message_id,json_extract(data,'$.info.time') message_time FROM event WHERE aggregate_id='ses_ef4efdc0bffeP1H6Ul9qC57zdH' AND seq>=8087 ORDER BY seq LIMIT 20;

SELECT count(*) examined_assistants,sum(CASE WHEN json_extract(m.data,'$.time.completed') IS NULL THEN 1 ELSE 0 END) incomplete_assistants FROM message m JOIN session s ON s.id=m.session_id WHERE s.project_id='3bc59309b6e8106fc20a1cab48de7d475c79f67e' AND s.parent_id IS NOT NULL AND m.time_created BETWEEN 1788739200000 AND 1791369846065 AND json_extract(m.data,'$.role')='assistant';

SELECT m.session_id,s.title,m.id,m.time_created,json_extract(m.data,'$.modelID') model,json_extract(m.data,'$.error') error FROM message m JOIN session s ON s.id=m.session_id WHERE s.project_id='3bc59309b6e8106fc20a1cab48de7d475c79f67e' AND s.parent_id IS NOT NULL AND m.time_created BETWEEN 1788739200000 AND 1791369846065 AND json_extract(m.data,'$.role')='assistant' AND json_extract(m.data,'$.time.completed') IS NULL ORDER BY m.time_created;

SELECT id,json_extract(data,'$.state.metadata.sessionId') child,json_extract(data,'$.state.status') status,json_extract(data,'$.state.time.start') start_ms,json_extract(data,'$.state.time.end') end_ms,round((json_extract(data,'$.state.time.end')-json_extract(data,'$.state.time.start'))/1000.0,3) duration_s FROM part WHERE session_id='ses_f0e3bd4e4ffem8jmapJbWHWjLz' AND json_extract(data,'$.tool')='task' AND json_extract(data,'$.state.metadata.sessionId') IN ('ses_ef4efdaacffesFcTKCaW6bIgLg','ses_eed992904ffetnnsCdZm0LOxUX','ses_eeb20c6a0ffeDCYxnnj59coD9g') ORDER BY time_created;

-- Follow-up: measure embedded media carrier length without exposing its value.
SELECT id,json_extract(data,'$.state.input.filePath') filePath,json_extract(data,'$.state.input.offset') offset,json_extract(data,'$.state.input.limit') requested_limit,length(json_extract(data,'$.state.attachments[0].url')) url_chars,json_extract(data,'$.state.status') status FROM part WHERE session_id='ses_ef4efdd58ffeU3uWpkKUMNHVWE' AND time_created>=1791195540000 AND json_extract(data,'$.tool')='read' AND json_extract(data,'$.state.input.filePath') LIKE '%.pdf' ORDER BY time_created;

SELECT json_type(data,'$.overflow') overflow_type,json_extract(data,'$.overflow') overflow,count(*) n FROM part WHERE session_id='ses_ef4efdd58ffeU3uWpkKUMNHVWE' AND time_created>=1791195540000 AND json_extract(data,'$.type')='compaction' GROUP BY json_type(data,'$.overflow'),json_extract(data,'$.overflow');

SELECT id,json_extract(data,'$.time.completed') completed_ms,json_extract(data,'$.finish') finish,json_extract(data,'$.error.name') error_name FROM message WHERE id IN ('msg_10b95da78001wjcI5A700aciD6','msg_10b996509001vMQMqqtZQA1Brr','msg_10b9da94a001ey3nAZ0Gd7K1YH','msg_10ba21e370010rnGZF1tYiVyKf','msg_10baad038001wVdke8EQkTJ2st');

SELECT id,time_created,time_updated,json_extract(data,'$.time') time,json_extract(data,'$.finish') finish FROM message WHERE id='msg_10bbbd23c001qh4ON51FQjsRPk';

SELECT id,json_extract(data,'$.state.status') status,json_extract(data,'$.state.time') time FROM part WHERE id IN ('prt_10bbcc323001wQ0UxWTt8Jp0NT','prt_10bbcc66e001i21VS7PBZ1Kcvd','prt_10bbcc7bb001slhdbnKn7ycw9P','prt_10b93b397001ZC7liEox0yEh0T');
