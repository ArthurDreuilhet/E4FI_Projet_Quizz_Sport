# Questions des Jeux Olympiques - Structure des données

## 📁 Fichier de données : `public/jo_questions.json`

Ce fichier contient 15 questions amusantes et surprenantes sur l'histoire des Jeux Olympiques, formatées pour être directement utilisées par l'API du quiz.

## 🔧 Structure de chaque question

```json
{
  "title": "Question JO X",           // Titre affiché (numérotation automatique)
  "text": "La question posée...",       // Texte de la question
  "image": "",                       // URL d'une image (optionnel, vide par défaut)
  "possibleAnswers": [               // Tableau des réponses possibles
    {
      "text": "Première réponse",      // Texte de la réponse
      "isCorrect": false             // true pour la bonne réponse, false pour les autres
    },
    {
      "text": "Deuxième réponse",
      "isCorrect": true              // Une seule réponse doit être correcte
    },
    // ... autres réponses (généralement 4 au total)
  ]
}
```

## 🎯 Utilisation dans l'interface d'administration

1. **Bouton "Ajouter les questions JO"** dans la page Admin
2. **Chargement automatique** : Le fichier JSON est lu depuis `/public/jo_questions.json`
3. **Attribution des positions** : Les questions sont ajoutées à la suite des questions existantes
4. **Création via API** : Chaque question est envoyée à l'API avec le format approprié

## ✨ Fonctionnalités

- **Gestion des positions** : Les questions sont automatiquement numérotées en fonction de celles déjà présentes
- **Validation** : Confirmation avant ajout pour éviter les ajouts accidentels
- **Feedback** : Affichage du nombre de questions ajoutées avec succès
- **Gestion d'erreurs** : Messages d'erreur explicites en cas de problème

## 📝 Modification des questions

Pour modifier les questions :
1. Ouvrir le fichier `public/jo_questions.json`
2. Modifier le contenu des questions, réponses ou ajouter de nouvelles questions
3. Respecter la structure JSON existante
4. S'assurer qu'une seule réponse par question a `"isCorrect": true`

## 🔄 Processus d'ajout automatique

1. L'utilisateur clique sur "Ajouter les questions JO"
2. Confirmation demandée
3. Chargement du fichier JSON depuis `/public/jo_questions.json`
4. Pour chaque question :
   - Attribution d'une position (questions.length + 1)
   - Envoi à l'API via `QuizApiService.create_question()`
   - Incrémentation du compteur de succès
5. Rechargement de la liste des questions
6. Affichage du résultat

Cette approche permet une gestion flexible et maintenable des questions prédéfinies, tout en gardant la logique d'ajout séparée du code de l'interface.
