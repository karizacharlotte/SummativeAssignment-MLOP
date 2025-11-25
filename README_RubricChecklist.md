Rubric checklist for full marks

- Video Demo (5 pts):
  - [ ] Camera on and audio clear showing prediction and retraining process

- Retraining Process (10 pts):
  - [ ] Upload + save uploaded files to `data/upload/` via `/upload`
  - [ ] Preprocessing of uploaded files using `src/preprocessing.py`
  - [ ] Retraining uses custom model saved at `models/model.h5` via `/retrain`

- Prediction Process (10 pts):
  - [ ] Single image prediction via API `/predict` and UI
  - [ ] Correct predicted label shown in demo

- Evaluation (10 pts):
  - [ ] Notebook contains preprocessing steps and at least 4 evaluation metrics
  - [ ] Show optimization techniques (early stopping, transfer learning)

- Deployment (10 pts):
  - [ ] Provide Dockerized app or public URL
  - [ ] Provide data insights / basic visualizations
