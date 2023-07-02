import React from "react";
import {List, ResourceContextProvider, SimpleList} from "react-admin";

export default () => (
  <ResourceContextProvider value="botusers">
    <List disableSyncWithLocation exporter={false}>
      <SimpleList
        primaryText={record => record.username}
        secondaryText={record => `${record.first_name} ${record.last_name}`}
        tertiaryText={record => new Date(record.updated_at).toLocaleDateString()}
        linkType={record => record.canEdit ? "edit" : "show"}
      />
    </List>
  </ResourceContextProvider>
);
