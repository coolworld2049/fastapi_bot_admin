import {Create, required, SimpleForm, TextInput} from "react-admin";

export const PostCreate = () => (
  <Create>
    <SimpleForm>
      <TextInput source="text" validate={[required()]}/>
      {/*<FileInput source="file" multiple>*/}
      {/*  <FileField source="src" title="title"/>*/}
      {/*</FileInput>*/}
    </SimpleForm>
  </Create>
);
