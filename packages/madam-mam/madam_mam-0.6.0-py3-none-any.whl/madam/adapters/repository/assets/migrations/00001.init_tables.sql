create table workflows
(
    id         varchar(255) not null,
    version    integer      not null,
    name       varchar(255) not null,
    content    xml          not null,
    sha256     varchar(64)  not null,
    timer      varchar(255),
    created_at timestamp    not null,
    PRIMARY KEY (id, version)
);

create table timers
(
    id               uuid         not null,
    start_at         timestamp    not null,
    end_at           timestamp,
    status           varchar(30)  not null,
    input            jsonb,
    workflow_id      varchar(255) not null,
    workflow_version integer      not null,
    date             timestamptz,
    repeat           integer,
    interval         interval,
    PRIMARY KEY (id),
    FOREIGN KEY (workflow_id, workflow_version) REFERENCES workflows (id, version) ON DELETE CASCADE
);

create table workflow_instances
(
    id               uuid         not null,
    start_at         timestamp    not null,
    end_at           timestamp,
    status           varchar(30)  not null,
    input            jsonb,
    output           jsonb,
    error            varchar(65535),
    workflow_id      varchar(255) not null,
    workflow_version integer      not null,
    PRIMARY KEY (id),
    FOREIGN KEY (workflow_id, workflow_version) REFERENCES workflows (id, version) ON DELETE CASCADE
);

create table jobs
(
    id                   uuid         not null,
    agent_id             varchar(255) not null,
    agent_type           varchar(255) not null,
    start_at             timestamp    not null,
    end_at               timestamp,
    status               varchar(30)  not null,
    headers              jsonb,
    input                jsonb        not null,
    output               jsonb,
    error                varchar(65535),
    workflow_instance_id uuid         not null,
    PRIMARY KEY (id),
    FOREIGN KEY (workflow_instance_id) REFERENCES workflow_instances (id) ON DELETE CASCADE
);

create table applications
(
    id              uuid           not null,
    name            varchar(255)   not null,
    version         varchar(30)    not null,
    arguments       varchar(65535) not null,
    start_at        timestamp      not null,
    end_at          timestamp,
    status          varchar(30)    not null,
    logs            text,
    container_id    varchar(255),
    container_error varchar(65535),
    job_id          uuid           not null,
    PRIMARY KEY (id),
    FOREIGN KEY (job_id) REFERENCES jobs (id) ON DELETE CASCADE
);

create table watchfolders
(
    id                          uuid           not null,
    path                        varchar(65535) not null,
    start_at                    timestamp,
    end_at                      timestamp,
    status                      varchar(30)    not null,
    re_files                    varchar(255),
    re_dirs                     varchar(255),
    added_workflow_id           varchar(255),
    added_workflow_version      integer,
    added_variables             jsonb,
    modified_workflow_id        varchar(255),
    modified_workflow_version   integer,
    modified_variables          jsonb,
    deleted_workflow_id         varchar(255),
    deleted_workflow_version    integer,
    deleted_variables           jsonb,
    added_items_key             varchar(255)  not null default 'watchfolder',
    modified_items_key          varchar(255)  not null default 'watchfolder',
    deleted_items_key           varchar(255)  not null default 'watchfolder',
    PRIMARY KEY (id),
    FOREIGN KEY (added_workflow_id, added_workflow_version) REFERENCES workflows (id, version) ON DELETE CASCADE,
    FOREIGN KEY (modified_workflow_id, modified_workflow_version) REFERENCES workflows (id, version) ON DELETE CASCADE,
    FOREIGN KEY (deleted_workflow_id, deleted_workflow_version) REFERENCES workflows (id, version) ON DELETE CASCADE
);

GRANT ALL ON TABLE workflows TO madam;
GRANT ALL ON TABLE timers TO madam;
GRANT ALL ON TABLE workflow_instances TO madam;
GRANT ALL ON TABLE jobs TO madam;
GRANT ALL ON TABLE applications TO madam;
GRANT ALL ON TABLE watchfolders TO madam;
