SELECT voices.date,
       voices.ckeckao,
       voices.checkword,
       voices.duration,
       servers.id as server_id,
       servers.name as server_name,
       servers.description as server_description,
       projects.name as project_name,
       projects.description as project_description
FROM   voices
JOIN servers
    ON servers.id = voices.server_id
JOIN projects 
    ON projects.id = voices.project_id;
