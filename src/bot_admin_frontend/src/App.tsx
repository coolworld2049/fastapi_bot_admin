import {Admin, Resource, ShowGuesser} from 'react-admin';
import {dataProvider} from './dataProvider';
import {authProvider} from './authProvider';
import {UserCreate, UserEdit, UserList} from "./pages/Menu/User";
import PersonIcon from '@mui/icons-material/Person';
import {BotUserList} from "./pages/Menu/BotUser";

export const App = () => (
  <Admin
    dataProvider={dataProvider}
    authProvider={authProvider}
  >
    <Resource
      options={{label: "Users"}}
      name="users/"
      list={UserList}
      edit={UserEdit}
      create={UserCreate}
      show={ShowGuesser}
      icon={PersonIcon}
    />
    <Resource
      options={{label: "Bot Users"}}
      name="bot/users/"
      list={BotUserList}
      show={ShowGuesser}
      icon={PersonIcon}
    />
  </Admin>
);

