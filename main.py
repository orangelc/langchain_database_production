from chains.qa_chain import build_sql_chain

if __name__ == "__main__":
    agent = build_sql_chain()

    while True:
        question = input("Pregunta sobre la base de datos: ")
        if question.lower() in ["salir", "exit", "quit"]:
            break
        response = agent.invoke({"input": question})
        print("\nRespuesta:")
        print(response["output"])
