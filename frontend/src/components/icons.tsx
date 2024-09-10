import { RectangleEllipsisIcon } from "lucide-react";

type IconProps = React.HTMLAttributes<SVGElement>;

export const Icons = {
  logo: (props: IconProps) => <RectangleEllipsisIcon {...props} />,
};
