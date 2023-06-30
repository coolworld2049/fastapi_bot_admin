import {AuthProvider} from 'react-admin';
import {authApi} from "../env";


type loginFormType = {
  username: string;
  password: string;
};

export const authProvider: AuthProvider = {
  login: async ({username, password}: loginFormType) => {
    const response = await authApi.loginAccessTokenApiV1LoginAccessTokenPost(
      username,
      password,
      "password"
    ).then(
      (response) => {
        if (response.status < 200 || response.status >= 300) {
          throw new Error(response.statusText);
        }
        localStorage.setItem("token", response.data.access_token);
        return response.data.access_token;
      }
    );
  },
  logout: () => {
    localStorage.removeItem('token');
    return Promise.resolve();
  },
  checkError: () => Promise.resolve(),
  checkAuth: () =>
    localStorage.getItem('token') ? Promise.resolve() : Promise.reject(),
  getPermissions: () => {
    return Promise.resolve(undefined);
  },
  getIdentity: () => {
    const persistedUser = localStorage.getItem('token');
    const user = persistedUser ? JSON.parse(persistedUser) : null;

    return Promise.resolve(user);
  },
};
