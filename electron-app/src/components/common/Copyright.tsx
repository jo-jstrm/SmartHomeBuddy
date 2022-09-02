import Link from "@mui/material/Link";
import Typography from "@mui/material/Typography";

export default function Copyright(props: any) {
  return (
    <Typography
      variant="body2"
      color="text.secondary"
      align="center"
      {...props}
    >
      {"Copyright © "}
      <Link color="inherit" href="https://github.com/jo-jstrm/SmartHomeBuddy">
        SmartHomeBuddy
      </Link>{" "}
      {new Date().getFullYear()}
      {"."}
    </Typography>
  );
}
