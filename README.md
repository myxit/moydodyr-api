# Moydodyr API
A better implementation of the ELS booking system.

<img src="./doc/images/Screenshot_20240518_152428_Firefox.jpg" alt="Old interface screenshot" width="200"/>

## Python Dev setup
A bit complex setup:
 - Python virutal environment is set up using the `asdf python plugin` and direnv

More details: https://dev.to/frost/how-i-set-up-my-python-projects-using-asdf-and-direnv-4o67
 - __NOTE__: it seems [this plugin](https://marketplace.visualstudio.com/items?itemName=mkhl.direnv) required for having nested VSCode terminal working

### Misc
Packages managed by the `poetry` package manager. Run `poetry install` in the project directory root.

## Plan
### Background runner
- [X] login
- [X] laundry selection
- [X] get selected laundry weekly bookings
- [ ] booking
- [ ] cancelling bookings
- [ ] continuos runner
### API
[X] GET /api/bookings
[ ] 
[ ] auth jwt endpoint
