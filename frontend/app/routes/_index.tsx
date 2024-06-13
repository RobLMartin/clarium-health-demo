import type { MetaFunction } from "@remix-run/node";
import Navigation from "../components/navigation";
import { Outlet } from "@remix-run/react";

export const meta: MetaFunction = () => {
  return [
    { title: "Inventory" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};

export default function Index() {
  return (
    <div className="flex">
      <div className="w-auto border-x dark:border-neutral-700">
        <Navigation />
      </div>
      <div className="w-full border-r dark:border-neutral-700">
        <Outlet />
      </div>
    </div>
  );
}
