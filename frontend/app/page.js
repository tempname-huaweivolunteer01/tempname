"use client";

import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Card from "@/components/ui/Card";


export default function Home() {
  return (
    <Card>
      <Input
        label="Nome"
        placeholder="Digite seu nome"
      />
      <Button onClick={() => alert("cliquei!")}>Salvar</Button>
    </Card>
  );
}