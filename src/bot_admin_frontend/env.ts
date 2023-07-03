import {Configuration, LoginApi, UsersApi, PostsApi, PostMediasApi} from "./src/generated";

const readAccessToken = async (): Promise<string> => {
  return localStorage.getItem("token") || "";
};

export const basePath: string | undefined = import.meta.env.VITE_REST_URL;

const apiConfig: Configuration = new Configuration({
  accessToken: readAccessToken,
  basePath,
});

export const authApi: LoginApi = new LoginApi(apiConfig);
export const userApi: UsersApi = new UsersApi(apiConfig);
export const postApi: PostsApi = new PostsApi(apiConfig);
