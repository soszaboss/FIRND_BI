import ChatBot from "react-chatbotify";

const MyChatBot = () => {
  const downLoadDiplome = "Comment télécharger mes diplômes ?";
  const accessRequest = "Comment voir les demandes d'accès à mes diplômes ?";
  const sendToInstitutionOrEmployer = "Puis-je partager mon diplôme avec une institution ou un employeur ?";
  const necessaryDocumentForSubmission = "Quels documents sont nécessaires pour soumettre un diplôme ?";
  const submissionDocumentState = "Comment suivre l'état de validation des diplômes soumis ?";

  const helpOptions = [
    downLoadDiplome,
    accessRequest,
    sendToInstitutionOrEmployer,
    necessaryDocumentForSubmission,
    submissionDocumentState,
  ];

  const flow = {
    start: {
      message: "Bonjour, je suis Sidy 👋! Bienvenue sur FIRND Bi, Comment puis-je vous aider ?",
      transition: { duration: 1000 },
      path: "show_options",
    },
    show_options: {
      options: helpOptions,
      chatDisabled: true,
      path: async (params) => {
        console.log("Process options triggered");
        console.log("User input:", params.userInput);

        let responseMessage;

        switch (params.userInput) {
          case downLoadDiplome:
            responseMessage = "Sélectionnez l'option \"Télécharger mes diplômes\" dans le menu principal. Vous verrez une liste de vos diplômes disponibles. Choisissez le diplôme que vous souhaitez télécharger et cliquez sur le bouton correspondant.";
            break;
          case accessRequest:
            responseMessage = "Allez dans la section \"Demandes d'accès\" depuis le tableau de bord. Vous verrez toutes les demandes d'accès à vos diplômes. Vous pouvez les approuver ou les refuser en cliquant sur les options correspondantes.";
            break;
          case sendToInstitutionOrEmployer:
            responseMessage = "Oui, vous pouvez partager vos diplômes. Sélectionnez \"Partager mon diplôme\" dans le menu principal, puis entrez l'adresse e-mail de l'institution ou de l'employeur avec qui vous souhaitez partager le diplôme. Le destinataire recevra un lien sécurisé pour accéder au document.";
            break;
          case necessaryDocumentForSubmission:
            responseMessage = "Vous pouvez consulter la liste des documents requis dans la section \"Documents requis\" du menu principal. Cela inclut généralement une copie du diplôme, une pièce d'identité valide et d'autres justificatifs selon le type de diplôme.";
            break;
          case submissionDocumentState:
            responseMessage = "Pour suivre l'état de validation des diplômes que vous avez soumis, allez dans la section \"État de validation\" sur votre tableau de bord. Vous verrez le statut de chaque diplôme, comme \"En cours de validation\", \"Validé\" ou \"Rejeté\".";
            break;
          default:
            responseMessage = "Désolé, je ne comprends pas votre message!";
        }

        console.log("Response message:", responseMessage);
        await params.injectMessage(responseMessage);
        return "prompt_again";
      },
    },
    prompt_again: {
      message: "Avez-vous besoin d’une autre aide ?",
      transition: { duration: 500 },
      path: "show_options",
    },
    unknown_input: {
      message: "Désolé, je ne comprends pas votre message! Si vous avez besoin d'aide supplémentaire, vous pouvez cliquer sur l'option Github et y ouvrir un problème ou visiter notre discord.",
      transition: { duration: 500 },
      path: "show_options",
    },
  };

  const options = {
    theme: {
      embedded: true,
      primaryColor: "#13ED9E",
      secondaryColor: "#2A2A2A",
    },
    chatHistory: {
      storageKey: "example_theming",
    },
  };

  return (
    <div>
      <ChatBot flow={flow} options={options} />
    </div>
  );
};

export default MyChatBot;
