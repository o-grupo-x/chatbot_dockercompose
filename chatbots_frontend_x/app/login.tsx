"use client";

import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/login", {
        email,
        password,
      });
      if (response.data.token) {
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("userId", response.data.user.id);
        router.push("/chat");  // Redireciona para a página de chat
      } else {
        alert("Login falhou");
      }
    } catch (error) {
      console.log(error);
      alert("Erro ao fazer login");
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-gray-900 text-white">
      <div className="w-full max-w-sm p-4 bg-gray-800 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold mb-4">Login</h2>
        <p className="mt-4 text-center">
  Não tem uma conta?{" "}
  <Link href="/register" className="text-blue-400 hover:underline">
    Cadastre-se aqui
  </Link>
</p>

        <input
          type="email"
          placeholder="Email"
          className="w-full p-2 mb-2 bg-gray-700 rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Senha"
          className="w-full p-2 mb-4 bg-gray-700 rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 hover:bg-blue-700 p-2 rounded"
        >
          Entrar
        </button>
      </div>
    </div>
  );
}
