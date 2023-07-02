import {
  ArrayField,
  BooleanField,
  BooleanInput,
  ChipField,
  Create,
  Datagrid,
  DateField,
  DeleteButton,
  Edit,
  FileField,
  FileInput,
  List,
  RichTextField,
  SaveButton,
  SimpleForm,
  SimpleShowLayout,
  SingleFieldList,
  TextField,
  TextInput,
  Toolbar,
  useNotify,
  useRecordContext,
  useRefresh
} from "react-admin";
import {ClearButtons, FormatButtons, RichTextInput, RichTextInputToolbar} from "ra-input-rich-text";
import dataProvider from "../dataProvider";
import React from "react";

export const PostPanel = () => {
  return (
    <SimpleShowLayout>
      <TextField source="id"/>
      <DateField source="updated_at" showTime={true}/>
    </SimpleShowLayout>
  )
};

export const PostList = (props: any) => {
  return (
    <List sort={{field: 'updated_at', order: 'DESC'}}
          debounce={1000}>
      <Datagrid
        rowClick="edit"
        bulkActionButtons={false}
        expand={<PostPanel {...props}/>}
        expandSingle={true}
      >
        <RichTextField source="text"/>
        <ArrayField source="files">
          <SingleFieldList>
            <ChipField source="title" size="small"/>
          </SingleFieldList>
        </ArrayField>
        <BooleanField source="is_published" label={"Published"}/>
        <DateField source="created_at" showTime={true}/>
      </Datagrid>
    </List>
  );
};

const PostPublishButton = (props: any) => {
  const refresh = useRefresh();
  const notify = useNotify();
  const record = useRecordContext(props);
  const handleSuccess = () => {
    dataProvider.create(`posts/${record.id}/publish`,
      {
        ...record.params,
      }
    ).then(r => {
      notify(`Post ${r.data.id} published!`, {type: 'success'})
      refresh()
    })
  };
  const handleError = (error: any) => {
    notify(`Post ${record.id} not published!${error}`, {type: 'error'})
    refresh()
  };
  return (<SaveButton
    {...props}
    label={"Publish"}
    mutationOptions={{onSuccess: handleSuccess, onError: handleError}}
    type={"button"}
    variant="outlined"
    alwaysEnable={!(record.is_published)}
  />);
};

const PostPublishToolbar = (props: any) => {
  return (
    <Toolbar {...props}>
      <SaveButton {...props}
      />
      <PostPublishButton {...props} variant="outlined" sx={{marginLeft: "10px"}}/>
      <DeleteButton variant={"text"} sx={{marginLeft: "10px"}}/>
    </Toolbar>
  )
};

const TgRichTextInputToolbar = () => {
  return (
    <RichTextInputToolbar>
      <FormatButtons/>
      <ClearButtons/>
    </RichTextInputToolbar>
  )
}
export const PostEdit = (props: any) => {
  return (
    <Edit {...props} redirect="edit">
      <SimpleForm toolbar={<PostPublishToolbar/>}>
        <TextInput source="id" disabled/>
        <BooleanInput source="is_published"/>
        <RichTextInput
          source="text"
          toolbar={<TgRichTextInputToolbar/>}
          fullWidth
        />
        <FileInput source="files" multiple>
          <FileField source="src" title="title" download target={"_blank"}/>
        </FileInput>
      </SimpleForm>
    </Edit>
  )
};


export const PostCreate = () => {
  return (
    <Create redirect={"edit"}>
      <SimpleForm>
        <TextInput source="id" disabled/>
        <RichTextInput
          source="text"
          toolbar={<TgRichTextInputToolbar/>}
          fullWidth
        />
        <FileInput source="files" multiple>
          <FileField source="src" title="title" download target={"_blank"}/>
        </FileInput>
      </SimpleForm>
    </Create>
  )
};
