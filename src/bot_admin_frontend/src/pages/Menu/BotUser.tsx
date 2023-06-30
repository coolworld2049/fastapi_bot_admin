import {Datagrid, DateField, FilterLiveSearch, List, SimpleShowLayout, TextField,} from "react-admin";


const BotUserPanel = (props: any) => (
  <SimpleShowLayout>
    <TextField source="id"/>
    <TextField source="username"/>
    <TextField source="first_name"/>
    <TextField source="last_name"/>
    <TextField source="language_code"/>
    <DateField source="updated_at"/>
  </SimpleShowLayout>
);

export const BotUserList = (props: any) => {
  const userFilters = [
    <FilterLiveSearch source="username" label={"Username"}/>,
  ];
  return (
    <List {...props} filters={userFilters}>
      <Datagrid
        bulkActionButtons={false}
        expand={BotUserPanel}
        expandSingle={true}
      >
        <TextField source="id"/>
        <TextField source="username"/>
        <DateField source="created_at"/>
      </Datagrid>
    </List>
  );
};
