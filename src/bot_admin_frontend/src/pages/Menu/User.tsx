import {
  BooleanField,
  Create,
  Datagrid,
  DateField,
  Edit, FilterLiveSearch,
  List,
  PasswordInput,
  required,
  SimpleForm,
  SimpleShowLayout,
  TextField,
  TextInput,
} from "react-admin";
import PublicIcon from "@mui/icons-material/Public";
import PublicOffIcon from "@mui/icons-material/PublicOff";

const UserPanel = (props: any) => (
  <SimpleShowLayout>
    <TextField source="id"/>
    <TextField source="username"/>
    <TextField source="telegram_id"/>
    <TextField source="full_name"/>
    <DateField source="updated_at"/>
    <BooleanField
      source="is_active"
      TrueIcon={PublicIcon}
      FalseIcon={PublicOffIcon}
      label={"Active"}
    />
  </SimpleShowLayout>
);


export const UserList = (props: any) => {
  const userFilters = [
    <FilterLiveSearch source="email" label={"Full Name"}/>,
    <FilterLiveSearch source="username" label={"Username"}/>,
    <FilterLiveSearch source="telgram_id" label={"Telegam Id"}/>,
  ];
  return (
    <List {...props} filters={userFilters}>
      <Datagrid
        rowClick="edit"
        bulkActionButtons={false}
        expand={UserPanel}
        expandSingle={true}
      >
        <TextField source="email"/>
        <DateField source="created_at"/>
      </Datagrid>
    </List>
  );
};

export const UserEdit = (props: any) => (
  <Edit {...props} redirect="list">
    <SimpleForm>
      <TextInput source="id" disabled/>
      <TextInput source="username"/>
      <TextInput source="telegram_id" label={"Telegram id"}/>
    </SimpleForm>
  </Edit>
);

export const UserCreate = (props: any) => {
  return (
    <Create {...props} redirect="list">
      <SimpleForm mode="onBlur" reValidateMode="onBlur">
        <TextInput source="email" validate={required()}/>
        <PasswordInput source="password" validate={required()}/>
        <TextInput source="username"/>
      </SimpleForm>
    </Create>
  );
};
