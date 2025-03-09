"use client";

import dynamic from "next/dynamic";

const Chatbot = dynamic(() => import("./chatbot"), { ssr: false });
const Login = dynamic(() => import("./login"));

export default function Page() {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  return (
    <div>
      {token ? <Chatbot /> : <Login />}
    </div>
  );
}
