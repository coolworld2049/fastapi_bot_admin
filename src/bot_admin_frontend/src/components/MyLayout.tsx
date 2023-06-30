import {
  AppBar,
  defaultTheme,
  Layout,
  Logout,
  MenuItemLink,
  ToggleThemeButton,
  usePermissions,
  UserMenu,
} from "react-admin";
import {ReactQueryDevtools} from "react-query/devtools";
import {Box, createTheme, Typography} from "@mui/material";

const MyUserMenu = (props: any) => {
  return (
    <UserMenu {...props}>
      <Logout key="logout"/>
    </UserMenu>
  );
};

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
  typography: {
    // Use the system font instead of the default Roboto font.
    fontFamily: [
      "-apple-system",
      "BlinkMacSystemFont",
      '"Segoe UI"',
      "Arial",
      "sans-serif",
    ].join(","),
  },
});

const MyAppBar = (props: any) => (
  <AppBar {...props} userMenu={<MyUserMenu/>}>
    <Box flex="1">
      <Typography variant="h6" id="react-admin-title"></Typography>
    </Box>
    <ToggleThemeButton lightTheme={defaultTheme} darkTheme={darkTheme}/>
  </AppBar>
);

const MyLayout = (props: any) => (
  <>
    <Layout {...props} appBar={MyAppBar}/>
    <ReactQueryDevtools initialIsOpen={false}/>
  </>
);

export default MyLayout;
