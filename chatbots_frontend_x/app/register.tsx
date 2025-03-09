"use client";

import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const router = useRouter();

  const handleRegister = async () => {
    if (password !== confirmPassword) {
      alert("As senhas não coincidem!");
      return;
    }

    try {
      const response = await axios.post("http://localhost:5000/register", {
        email,
        password,
      });

      if (response.status === 201) {
        alert("Cadastro realizado com sucesso!");
        router.push("/login");
      } else {
        alert("Erro ao cadastrar.");
      }
    } catch (error) {
      console.log(error);
      alert("Erro ao cadastrar usuário.");
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-gray-900 text-white">
      <div className="w-full max-w-sm p-4 bg-gray-800 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold mb-4">Cadastrar</h2>
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
          className="w-full p-2 mb-2 bg-gray-700 rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="password"
          placeholder="Confirmar Senha"
          className="w-full p-2 mb-4 bg-gray-700 rounded"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
        <button
          onClick={handleRegister}
          className="w-full bg-blue-600 hover:bg-blue-700 p-2 rounded"
        >
          Cadastrar
        </button>
      </div>
    </div>
  );
}
