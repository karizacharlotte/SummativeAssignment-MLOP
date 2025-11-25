# Development Notes

Just some notes I kept while building this project.

## Challenges I Faced

1. **Memory Issues**: The full PathMNIST dataset (89k images) was too much for my laptop. Had to limit to 5000 samples during training. Works fine for the demo though!

2. **Model Selection**: Initially tried building a CNN from scratch but accuracy was only ~60%. Switched to transfer learning with MobileNetV2 and got 75%+ - much better!

3. **API Design**: Wasn't sure how to handle retraining without blocking the API. Found out about FastAPI's BackgroundTasks which is perfect for this.

4. **Docker Build**: First Docker build failed because I forgot to include the data directory. Fixed by adding proper COPY commands.

## Things That Worked Well

- Transfer learning really helped - MobileNetV2 gave me good accuracy with minimal training
- Early stopping prevented overfitting (validation accuracy was actually higher than training sometimes)
- Streamlit was super easy to build the UI with - way simpler than Flask
- The MedMNIST library made dataset handling really convenient

## What I'd Do Differently

- Could try fine-tuning the base model layers for even better accuracy
- Add data augmentation (rotations, flips) to improve generalization
- Implement proper logging instead of print statements
- Add user authentication for the retraining endpoint
- Use a proper database instead of just saving files to disk

## Resources That Helped

- MedMNIST paper and documentation
- FastAPI docs (especially BackgroundTasks)
- TensorFlow transfer learning tutorial
- Stack Overflow (as always!)

## Time Spent

- Dataset exploration and EDA: ~3 hours
- Model experimentation: ~5 hours (including training time)
- API development: ~2 hours
- UI development: ~2 hours
- Documentation and cleanup: ~2 hours
- Total: ~14 hours

## For Next Time

- Start the documentation earlier instead of at the end
- Test Docker build more frequently
- Keep better track of experiment results (should have used MLflow or something)
- Record the demo video earlier before you're tired!

---

*These are just my personal notes - feel free to ignore!*
