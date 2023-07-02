import {
  ChipField,
  Datagrid,
  DateField,
  FilterLiveSearch,
  List,
  SimpleShowLayout,
  TextField,
  useRecordContext,
} from "react-admin";

const BotUserPanel = (props: any) => (
  <SimpleShowLayout>
    <TextField source="id"/>
    <TextField source="first_name"/>
    <TextField source="last_name"/>
    <TextField source="language_code"/>
    <DateField source="updated_at"/>
  </SimpleShowLayout>
);

export const BotUserList = (props: any) => {
  const record = useRecordContext();

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
        <ChipField source="username"/>
        <DateField source="created_at"/>
      </Datagrid>
    </List>
  );
};

