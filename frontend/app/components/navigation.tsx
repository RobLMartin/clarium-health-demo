import NavItem from "./nav.item";
import { ListBulletIcon, HomeIcon } from "@radix-ui/react-icons";
import Logo from "./logo";

export default function Navigation() {
  return (
    <div className="h-screen">
      <div className="flex-grow flex flex-col justify-end items-center">
        <NavItem to="/" icon={<Logo height={30} width={30} />} title="" />
        <NavItem
          to={`/`}
          icon={<HomeIcon height={28} width={28} />}
          title="Home"
        />
        <NavItem
          to={`/products`}
          icon={<ListBulletIcon height={28} width={28} />}
          title="Products"
        />
      </div>
    </div>
  );
}
