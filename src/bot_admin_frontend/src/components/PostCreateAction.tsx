import React from "react";
import {Button} from "@mui/material";
import {postApi} from "../../env";

export const PostCreateAction = () => {
  const [cipher, setCipher] = React.useState("");

  const handleSubmit = (event: { preventDefault: () => void }) => {
    event.preventDefault();
    const newOption = {cph: cipher};
    postApi
      .publishPostApiV1PostsIdPost(id)
  };

  return (
    <Button onClick={handleSubmit}>Cancel</Button>
  );
};
