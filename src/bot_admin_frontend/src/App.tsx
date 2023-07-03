import {Admin, Resource, Show, ShowGuesser} from 'react-admin';
import {authProvider} from './authProvider';
import {UserCreate, UserEdit, UserList} from "./pages/User";
import PersonIcon from '@mui/icons-material/Person';
import {BotUserList} from "./pages/BotUser";
import {PostCreate, PostEdit, PostList, PostPanel} from "./pages/Post";
import dataProvider from "./dataProvider";
import PostAddIcon from '@mui/icons-material/PostAdd';
import TelegramIcon from '@mui/icons-material/Telegram';
import {darkTheme} from "./theme/Theme";
import Dashboard from "./pages/Dashboard";

export const App = () => (
  <Admin
    dataProvider={dataProvider}
    authProvider={authProvider}
    darkTheme={darkTheme}
    requireAuth
    dashboard={Dashboard}
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

