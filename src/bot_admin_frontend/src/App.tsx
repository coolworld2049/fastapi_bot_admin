import {Admin, ListGuesser, Resource, ShowGuesser} from 'react-admin';
import {authProvider} from './authProvider';
import {UserCreate, UserEdit, UserList} from "./pages/Menu/User";
import PersonIcon from '@mui/icons-material/Person';
import {BotUserList} from "./pages/Menu/BotUser";
import {PostCreate} from "./pages/Menu/Post";
import dataProvider from "./dataProvider";
import MyLayout from "./components/MyLayout";


export const App = () => (
  <Admin
    dataProvider={dataProvider}
    authProvider={authProvider}
    layout={MyLayout}
  >
    <Resource
      options={{label: "Users"}}
      name="users"
      list={UserList}
      edit={UserEdit}
      create={UserCreate}
      show={ShowGuesser}
      icon={PersonIcon}
    />
    <Resource
      options={{label: "Bot Users"}}
      name="bot/users"
      list={BotUserList}
      show={ShowGuesser}
      icon={PersonIcon}
    />
    <Resource
      options={{label: "Posts"}}
      name="bot/posts"
      list={ListGuesser}
      create={PostCreate}
      icon={PersonIcon}
    />
  </Admin>
);

