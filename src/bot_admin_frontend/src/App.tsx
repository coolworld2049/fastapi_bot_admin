import {Admin, EditGuesser, Resource, Show, ShowGuesser} from 'react-admin';
import {authProvider} from './authProvider';
import {UserCreate, UserEdit, UserList} from "./pages/Menu/User";
import PersonIcon from '@mui/icons-material/Person';
import {BotUserList} from "./pages/Menu/BotUser";
import {PostCreate, PostEdit, PostList, PostPanel} from "./pages/Menu/Post";
import dataProvider from "./dataProvider";
import MyLayout from "./components/MyLayout";
import PostAddIcon from '@mui/icons-material/PostAdd';
import TelegramIcon from '@mui/icons-material/Telegram';

export const App = () => (
  <Admin
    dataProvider={dataProvider}
    authProvider={authProvider}
    layout={MyLayout}
    requireAuth
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
      name="botusers"
      list={BotUserList}
      show={ShowGuesser}
      icon={TelegramIcon}
    />
    <Resource
      options={{label: "Posts"}}
      name="posts"
      list={PostList}
      edit={PostEdit}
      show={
        <Show>
          <PostPanel/>
        </Show>
      }
      create={PostCreate}
      icon={PostAddIcon}
    />
  </Admin>
);

